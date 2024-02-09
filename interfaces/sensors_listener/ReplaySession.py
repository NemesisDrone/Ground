import threading
import time
from typing import Union, List

from apps.replay.models import ReplaySession, ReplaySessionData
from django.utils import timezone

from CommunicationHandler import CommunicationLayer


class ReplaySessionManager(CommunicationLayer):
    def __init__(self):
        """
        This class is used to manage the replay session
        """
        super().__init__()
        self._is_recording = False
        self._is_paused = False
        # Time in tenths of seconds
        self._time_index = 0
        self._last_recording_time = time.time() * 10

        self.session: Union[None, ReplaySession] = None
        self._current_session_data: Union[None, ReplaySessionData] = None
        self._last_session_data: Union[None, ReplaySessionData] = None

        self._sessions_data_bulk: List[ReplaySessionData] = []

        self._session_time_thread = threading.Thread(
            target=self._handle_session_time_thread,
            daemon=True,
        )
        self._session_time_thread.start()

    def _send_status_to_frontend(self):
        """
        This method is used to send the status of the recorder to the frontend
        """
        self.send_to_frontend(
            {
                "type": "recorder:status",
                "data": {
                    "is_recording": self._is_recording,
                    "is_paused": self._is_paused,
                },
            }
        )

    def start_recording(self):
        """
        This method is used to start the replay session
        """
        print("Recording started")
        if self._is_paused and self._is_recording:
            self._is_paused = False
            self._send_status_to_frontend()
            return

        self.session = ReplaySession.objects.create(
            start_time=timezone.now(),
        )
        self.session.name = f"Replay session {self.session.id}"
        self.session.save()

        self._is_recording = True
        self._time_index = 0
        self._send_status_to_frontend()

    def pause_recording(self):
        """
        This method is used to pause the replay session
        We save data.
        """
        print("Recording paused")
        self._is_paused = True

        self._send_status_to_frontend()

        self._save_bulk_session_data()

    def stop_recording(self):
        """
        This method is used to stop the replay session
        We save data.
        """
        print("Recording stopped")
        if self.session:
            self.session.end_time = timezone.now()
            self.session.save()
            self.session = None

        self._is_recording = False
        self._is_paused = False
        self._save_bulk_session_data()

        self._send_status_to_frontend()

    def _handle_session_time_thread(self):
        """
        This method is used to handle the time of the replay session and to
        automatically call the bulk session saving
        """
        while True:
            current_time = time.time() * 10
            if not self._is_recording or self._is_paused:
                time.sleep(0.1)
                continue

            if len(self._sessions_data_bulk) > 20:
                self._save_bulk_session_data()

            if (current_time - self._last_recording_time) > 1:
                self._last_recording_time = current_time

                if self._current_session_data:
                    self._last_session_data = self._current_session_data
                    self._sessions_data_bulk.append(self._current_session_data)

                self._current_session_data = ReplaySessionData(
                    session=self.session,
                    index=self._time_index,
                )

                if self._last_session_data:
                    self._current_session_data.altitude = (
                        self._last_session_data.altitude
                    )
                    self._current_session_data.latitude = (
                        self._last_session_data.latitude
                    )
                    self._current_session_data.longitude = (
                        self._last_session_data.longitude
                    )
                    self._current_session_data.speed = self._last_session_data.speed
                    self._current_session_data.roll = self._last_session_data.roll
                    self._current_session_data.pitch = self._last_session_data.pitch
                    self._current_session_data.yaw = self._last_session_data.yaw
                else:
                    self._current_session_data.altitude = 100
                    self._current_session_data.speed = 12
                    self._current_session_data.latitude = -0.7563779
                    self._current_session_data.longitude = 48.0879123

                self._time_index += 10

            time.sleep(0.03)

        # if self._last_recording_time

    def _save_bulk_session_data(self):
        """
        This method is used to save the data of the replay session
        To improve the performance, we save the data in bulk
        """

        if len(self._sessions_data_bulk) == 0:
            return

        ReplaySessionData.objects.bulk_create(self._sessions_data_bulk)
        self._sessions_data_bulk = []

        print("Bulk saved")

    def add_update_data(self, data: dict):
        """
        This method is used to add or update the data of the replay session
        Every x seconds, we save the data in bulk
        """
        if not self._is_recording or self._is_paused:
            return

        message_type = data["type"]
        data = data["data"]

        match message_type:
            case "sensors:sense_hat:data":
                self._current_session_data.roll = data["roll"]
                self._current_session_data.pitch = data["pitch"]
                self._current_session_data.yaw = data["yaw"]

            case "sensors:altitude":
                self._current_session_data.altitude = data["altitude"]
