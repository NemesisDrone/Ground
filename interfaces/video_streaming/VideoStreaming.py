#!/usr/bin/python3

import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject as gobject, Gst

import threading
import asyncio as aio
from websockets.server import serve as wss
from websockets import exceptions as wssexcept
from websockets.server import WebSocketServerProtocol as wssp


# [TODO] See if it's worth switching back to H264.
# Don't forget to look at the legacy code for H264 in case of switch back.
# All the previous code that was used for H264 has the [LEGACY] tag.

# [LEGACY] H264 Works
#RECEIVED_FORMAT = "video/x-h264,profile=baseline,stream-format=byte-stream"
#DECODE_PIPELINE = "appsrc name=src ! openh264dec ! jpegenc ! appsink name=sink sync=false drop=True emit-signals=True"
DECODE_PIPELINE = "appsrc name=src ! appsink name=sink emit-signals=True"


async def functionWrap(func):
    await func()


class NVSState(int):
    """
    @brief Class representing the different states of NVSComponent.
    """
    GstInitFail: int = 0
    PipelineCreationFail: int = 1
    SinkLookupFail: int = 2
    SrcLookupFail: int = 3
    GstFlowError: int = 4
    GstBufferFail = 5
    Initialized: int = 6
    WaitingConnection: int = 7
    Streaming: int = 8
    Cleaning: int = 9
    Unknown: int = 10
    PendingStop: int = 11


class NVSServer:
    def __init__(self) -> None:
        self.clients: list = []
        self.pendingBuffers: list = []
        self.nvs_state: int = NVSState.Unknown
        self.waiting: tuple = None
        self.lastSender: wssp = None
        self.push_waiting: bytes = None
        self.enable_src_push = False
        self.cthread: threading.Thread = None
        self.cloop: aio.AbstractEventLoop = None

        """
        [LEGACY] H264 Works
        if not Gst.init_check(None): # init gstreamer
            self.log("GST init failed!", ll.CRITICAL)
            self.set_nvs_state(NVSState.GstInitFail)
            return

        global DECODE_PIPELINE
        global RECEIVED_FORMAT

        self.pipeline = Gst.parse_launch(DECODE_PIPELINE)
        if not self.pipeline:
            self.set_nvs_state(NVSState.PipelineCreationFail)
            return

        self.sink = self.pipeline.get_by_name("sink")
        if not self.sink:
            self.set_nvs_state(NVSState.SinkLookupFail)
            return

        self.src = self.pipeline.get_by_name("src")
        if not self.src:
            self.set_nvs_state(NVSState.SrcLookupFail)
            return

        # Notify us when it receives a frame
        self.sink.set_property("emit-signals", True)
        # Set CB for new data
        self.sink.connect("new-sample", self._on_output_available)

        # Setup our appsrc.
        self.src.set_property("format", Gst.Format.TIME)
        #self.src.set_property("caps", Gst.Caps.from_string(RECEIVED_FORMAT))
        #self.src.set_property("block", True) # So we can drop frames as needed.
        self.src.connect("need-data", self._on_data_needed)
        self.src.connect("enough-data", self._on_enough_data)"""

        self.set_nvs_state(NVSState.Initialized)


    def __del__(self) -> None:
        self.stop()


    def set_nvs_state(self, val) -> None:
        if int(val) < int(NVSState.Initialized):
            print("Warning, state:" + str(val))
        self.nvs_state = val


    def stop(self) -> None:
        self.set_nvs_state(NVSState.PendingStop)
        for sock in self.clients:
            sock.close()

        """
        [LEGACY] H264 Works
        self.clear_waiting_data()

        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)"""

        self.set_nvs_state(NVSState.Initialized)


    async def run(self) -> None:
        def loop_setter(loop):
            aio.set_event_loop(loop)
            loop.run_forever()

        if self.nvs_state != NVSState.Initialized:
            return

        """
        [LEGACY] H264 Works
        self.pipeline.set_state(Gst.State.PLAYING)

        self.loop = aio.new_event_loop()
        aio.set_event_loop(self.loop)
        self.thread = threading.Thread(target=loop_setter, args=(self.loop,))
        self.thread.start()

        aio.run_coroutine_threadsafe(functionWrap(self._data_push_loop), self.loop)"""

        await self._connection_loop()


    async def _connection_loop(self) -> None:
        if self.nvs_state != NVSState.Initialized:
            return

        print("NVS Server up and running.")

        while self.nvs_state != NVSState.PendingStop:
            try:
                async with wss(self._handle_connection, "0.0.0.0", port=7000):  # [TODO] See what address to use.
                    self.set_nvs_state(NVSState.WaitingConnection)
                    await aio.Future()
            except Exception:
                pass


    async def _handle_connection(self, sock: wssp) -> None:
        print("Client connected to NVS Server.")
        self.set_nvs_state(NVSState.Streaming)
        self.clients.append(sock)
        try:
            while self.nvs_state != NVSState.PendingStop:
                try:
                    data = await sock.recv()

                    # Send through APPSRC
                    #self.push_waiting = data

                    if self.lastSender != sock:
                        self.lastSender = sock

                    for socket in self.clients:
                        if socket != self.lastSender:
                            await socket.send(data)

                finally:
                    pass

            await sock.close()

        except wssexcept.ConnectionClosed:
            pass

        if sock in self.clients:
            self.clients.remove(sock)


    #
    #  The followings methods are legacy from H264 works. Leave it here in case we switch back from JPEG to H264 streaming.
    # [LEGACY] H264 Works
    #


    """def _on_data_needed(self, appsrc, u_size) -> None:
        self.enable_src_push = True


    def _on_enough_data(self):
        self.enable_src_push = False


    def _data_push_loop(self) -> None:
        while self.nvs_state != NVSState.PendingStop:
            if self.enable_src_push:
                if self.push_waiting:
                    ret = Gst.FlowReturn.OK
                    inner = bytearray(self.push_waiting)
                    buff = Gst.Buffer.new_wrapped_data(inner)
                    # Send through APPSRC
                    self.src.emit("push-buffer", buff, ret)
                    buff.unref()
                    self.push_waiting = None

                    print("Pushed data.")

                    if ret != Gst.FlowReturn.OK:
                        self.set_nvs_state(NVSState.GstFlowError)

    def _on_output_available(self, appsink) -> None:
        ""
        Handles incoming data from a GST pipeline.
        ""
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


    async def _push(self, stuff: tuple) -> None:
        print("Forwarding")
        # Stream to other clients.
        for sock in self.clients:
            if sock != self.lastSender:
                await sock.send(stuff[1].data)
                stuff[0].unmap(stuff[1])


    def clear_waiting_data(self) -> None:
        ""
        Clears all the data put in the pending list for sending.
        ""
        f, self.waiting = self.waiting, None
        f[0].unmap(f[1])"""


    def get_nvs_state(self) -> int:
        return self.nvs_state


nvss = NVSServer()
aio.run(nvss.run())
