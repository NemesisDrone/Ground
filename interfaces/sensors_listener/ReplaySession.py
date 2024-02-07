from typing import Union

from apps.replay.models import ReplaySession
from django.utils import timezone

from CommunicationHandler import CommunicationLayer


class ReplaySessionManager(CommunicationLayer):
    def __init__(self):
        """
        This class is used to manage the replay session
        """
        super().__init__()
        self.session: Union[None, ReplaySession] = None
        self._is_recording = False
        self._is_paused = False

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

        self._is_recording = True
        self._send_status_to_frontend()

        self.session = ReplaySession.objects.create(
            start_time=timezone.now(),
        )
        self.session.name = f"Replay session {self.session.id}"
        self.session.save()

    def pause_recording(self):
        """
        This method is used to pause the replay session
        """
        print("Recording paused")
        self._is_paused = True

        self._send_status_to_frontend()

    def stop_recording(self):
        """
        This method is used to stop the replay session
        """
        print("Recording stopped")
        self.session.end_time = timezone.now()
        self.session.save()
        self.session = None

        self._is_recording = False
        self._is_paused = False

        self._send_status_to_frontend()
