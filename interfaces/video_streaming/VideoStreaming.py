#!/usr/bin/python3

import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject as gobject, Gst

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

        self.set_nvs_state(NVSState.Initialized)


    def __del__(self) -> None:
        self.stop()


    def set_nvs_state(self, val) -> None:
        """
        Setter for the object's internal state. Also implements guards to log unproper behaviours.
        :param val: Integer corresponding to a NVSState.
        """
        if int(val) < int(NVSState.Initialized):
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
        """
        Handles the connection established with a client.
        :param sock: Websocket for the client that just connected.
        """
        print("Client connected to NVS Server.")
        self.set_nvs_state(NVSState.Streaming)
        self.clients.append(sock)
        try:
            while self.nvs_state != NVSState.PendingStop:
                try:
                    data = self._process_data(await sock.recv())

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

    @staticmethod
    async def _process_data(data: bytes) -> bio:
        """
        This function adds EXIF data to the input image :param data, and returns the updated data.
        :param data: Raw JPEG data
        :return: Raw JPEG data with EXIF.
        """
        # Load as the data was a file.
        output_buff = bio()
        exif.set_gps_location(data, 0.0, 0.0, 0.0, output_buff)
        return output_buff


    def get_nvs_state(self) -> int:
        """
        Retrieves the internal state of the object.
        :return: Integer corresponding to an NVSState.
        """
        return self.nvs_state


nvss = NVSServer()
aio.run(nvss.run())
