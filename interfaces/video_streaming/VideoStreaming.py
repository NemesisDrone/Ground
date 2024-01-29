#!/usr/bin/python3

import os
import gi

gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gst

import threading
import asyncio as aio
from websockets import exceptions as wssexcept
from websockets.server import serve as wss
from websockets.server import WebSocketServerProtocol as wssp

from io import BytesIO as bio
import exif


async def functionWrap(func):
    await func()


class NVSState(int):
    """
    @brief Class representing the different states of NVSComponent.
    """

    GstInitFail: int = 0
    PipelineCreationFail: int = 1
    SinkLookupFail: int = 2
    GstBufferFail = 3
    Unknown: int = 4
    Initialized: int = 5
    WaitingConnection: int = 6
    PendingStop: int = 7


class NVSServer:
    def __init__(self) -> None:
        self.clients: dict = {}  # List of connected clients plus their pending frames

        self.nvs_state: int = NVSState.Unknown
        self.lastSender: wssp = None

        self.thread: threading.Thread = None
        self.loop: aio.AbstractEventLoop = None

        if not Gst.init_check(None):  # init gstreamer
            self.print("GST init failed!")
            self.set_nvs_state(NVSState.GstInitFail)
            return

        # Setting GST's logging level to output.
        # see https://gstreamer.freedesktop.org/documentation/tutorials/basic/debugging-tools.html
        # Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)

        gst_pipeline_str = "udpsrc port=7001 caps="
        gst_pipeline_str += '"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96"'
        gst_pipeline_str += " ! rtph264depay ! h264parse ! avdec_h264 ! queue "
        gst_pipeline_str += " ! videoconvert ! jpegenc ! appsink name=sink"

        self.pipeline = Gst.parse_launch(gst_pipeline_str)

        if not self.pipeline:
            print("Could not create pipeline.")
            self.set_nvs_state(NVSState.PipelineCreationFail)
            return

        self.sink = self.pipeline.get_by_name("sink")
        if not self.sink:
            print("Could not find pipeline sink.", self.NAME)
            self.set_nvs_state(NVSState.SinkLookupFail)
            return

        # Notify us when it receives a frame
        self.sink.set_property("emit-signals", True)
        # Set CB for new data
        self.sink.connect("new-sample", self._on_data_available)

        print("Initialized.")
        self.set_nvs_state(NVSState.Initialized)

    def __del__(self) -> None:
        self.stop()

    def set_nvs_state(self, val) -> None:
        """
        Setter for the object's internal state. Also implements guards to log unproper behaviours.
        :param val: Integer corresponding to a NVSState.
        """
        if val < NVSState.Initialized:
            print("Warning, state:" + str(val))
        self.nvs_state = val

    def stop(self) -> None:
        """
        Stops the running loops & connections.
        This will stop the possibility to try to connect to the address too.
        """
        self.set_nvs_state(NVSState.PendingStop)
        for sock in self.clients:
            sock.close()

        self.pipeline.set_state(Gst.State.NULL)
        self.set_nvs_state(NVSState.Initialized)

    async def run(self) -> None:
        """
        Starts event loop to enable WS connections.
        """
        if self.nvs_state != NVSState.Initialized:
            return

        await self._connection_loop()

    async def _connection_loop(self) -> None:
        """
        Function generating a loop, waiting for new clients to connect and handles it.
        """
        self.pipeline.set_state(Gst.State.PLAYING)
        print("NVS Server up and running.")

        while self.nvs_state != NVSState.PendingStop:
            try:
                async with wss(self._handle_connection, "0.0.0.0", port=7000):
                    self.set_nvs_state(NVSState.WaitingConnection)
                    await aio.Future()
            finally:
                pass

    async def _handle_connection(self, sock):
        print("Client connected")
        self.clients[sock] = []

        try:
            while True:
                if len(self.clients[sock]) > 0:
                    buff = self.clients[sock].pop(0)
                    await sock.send(buff)
        except wssexcept.ConnectionClosed:
            del self.clients[sock]

    def _on_data_available(self, appsink):
        """
        Handles incoming data from a GST pipeline and buffers it. If new data is available but the previous has not
        been sent, the previous is dropped and the new one will be scheduled for sending.
        """
        sample = appsink.emit("pull-sample")

        if sample:
            gst_buffer = sample.get_buffer()
            try:
                (ret, buffer_map) = gst_buffer.map(Gst.MapFlags.READ)
                if ret:
                    # Pending for all clients.
                    for cli in self.clients.items():
                        if True:  # Frame not scheduled as there's no more space.
                            cli[1].append(bytes(buffer_map.data))
                    # Just release this frame.
                    gst_buffer.unmap(buffer_map)
                else:
                    self.set_nvs_state(NVSState.GstBufferFail)

            finally:
                pass

        return Gst.FlowReturn.OK


nvss = NVSServer()
aio.run(nvss.run())
