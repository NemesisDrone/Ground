#!/usr/bin/python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject as gobject, Gst

import dataclasses
from enum import Enum
import asyncio as aio
from websockets.server import serve as wss
from websockets import exceptions as wssexcept


DECODE_PIPELINE = "appsrc name=src ! openh264dec ! jpegenc ! appsink name=sink sync=false drop=True emit-signals=True"
RECEIVED_FORMAT = "video/x-h264,profile=baseline,stream-format=byte-stream"


@dataclasses.dataclass
class NVSState(Enum):
    """
    @brief Class representing the different states of NVSComponent.
    """
    GstInitFail: int = 0
    PipelineCreationFail: int = 1
    SinkLookupFail: int = 2
    Initialized: int = 3
    WaitingConnection: int = 4
    Streaming: int = 5
    Cleaning: int = 6
    Unknown: int = 7
    PendingStop: int = 8
    SrcLookupFail: int = 9
    GstFlowError: int = 10


class NVSServer:
    def __init__(self):
        self.clients = []
        self.nvs_state = NVSState.Unknown
        self.waiting = None
        self.server = None
        self.lastSender = None

        if not Gst.init_check(None): # init gstreamer
            self.log("GST init failed!", ll.CRITICAL)
            self.nvs_state = NVSState.GstInitFail
            return

        global DECODE_PIPELINE
        global RECEIVED_FORMAT

        self.pipeline = Gst.parse_launch(DECODE_PIPELINE)
        if not self.pipeline:
            self.nvs_state = NVSState.PipelineCreationFail
            return

        self.sink = self.pipeline.get_by_name("sink")
        if not self.sink:
            self.nvs_state = NVSState.SinkLookupFail
            return

        self.src = self.pipeline.get_by_name("src")
        if not self.src:
            self.nvs_state = NVSState.SrcLookupFail
            return

        # Notify us when it receives a frame
        self.sink.set_property("emit-signals", True)
        # Set CB for new data
        self.sink.connect("new-sample", self._on_output_available)

        # Setup our appsrc.
        self.src.set_property("format", Gst.Format.TIME)
        #self.src.set_caps(Gst.Caps.from_string(RECEIVED_FORMAT))
        self.src.set_property("caps", Gst.Caps.from_string(RECEIVED_FORMAT))
        #self.src.set_property("block", True) # So we can drop frames as needed.

        self.nvs_state = NVSState.Initialized


    def __del__(self):
        self.stop()

    def stop(self):
        self.nvs_state = NVSState.PendingStop
        for wss in self.clients:
            wss.close()

        self.clear_waiting_data()

        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)

        self.log("Stopped.", ll.INFO)
        self.nvs_state = NVSState.Initialized


    async def run(self):
        if self.nvs_state != NVSState.Initialized:
            return

        self.pipeline.set_state(Gst.State.PLAYING)
        async with wss(self._handle_connection, "172.20.10.2", port=7000): # [TODO] See what address to use.
            self.nvs_state = NVSState.WaitingConnection
            await aio.Future()


    async def _handle_connection(self, wss):
        self.nvs_state = NVSState.Streaming
        print("Connection acquired!")
        try:
            while self.nvs_state != NVSState.PendingStop:
                #try:
                data = await wss.recv()
                ret = Gst.FlowReturn.OK
                buff = Gst.Buffer.new_wrapped(data)
                # Send through APPSRC
                self.src.emit("push-buffer", buff, ret)
                buff.unref()

                if ret != Gst.FlowReturn.OK:
                    self.nvs_state = NVSState.GstFlowError

                if self.lastSender != wss:
                    self.lastSender = wss

            await wss.close()

        except wssexcept.ConnectionClosedOK:
            pass

        if wss in self.clients:
            self.clients.remove(wss)


    def _on_output_available(self, appsink):
        """
        Handles incoming data from a GST pipeline.
        """
        print("Pulling")
        sample = appsink.emit("pull-sample")

        if sample:
            gst_buffer = sample.get_buffer()
            try:
                (ret, buffer_map) = gst_buffer.map(Gst.MapFlags.READ)
                if self.waiting:
                    self.waiting[0].unmap(self.waiting[1])

                if self.clients: # Would be useless to store frames while there is no conn.
                    self.waiting = (gst_buffer, buffer_map)

            finally:
                self._push(self.waiting)

        return Gst.FlowReturn.OK


    async def _push(self, stuff):
        print("Forwarding")
        # Stream to other clients.
        for wss in self.clients:
            if wss != self.lastSender:
                await wss.send(stuff[1].data)
                stuff[0].unmap(stuff[1])


    def clear_waiting_data(self):
        """
        Clears all the data put in the pending list for sending.
        """
        f, self.waiting = self.waiting, None
        f[0].unmap(f[1])


    def get_nvs_state(self):
        return self.nvs_state


nvss = NVSServer()
aio.run(nvss.run())
