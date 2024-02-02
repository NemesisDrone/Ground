import json
import os
import threading
from typing import Union
import DjangoSetup

import redis
from apps.replay.models import ReplaySession
from django.utils import timezone


class SensorsListener:
    """
    This class is used to listen to sensors data and save it in a replay session when recording
    """

    def __init__(self):
        self._is_recording = False
        # Only used when recording is paused
        self._is_paused = False
        self.replay: Union[ReplaySession, None] = None
        self.redis = redis.StrictRedis(
            host=os.environ.get("REDIS_HOST"),
            port=os.environ.get("REDIS_PORT"),
            db=0,
            decode_responses=True,
        )
        self.redis_actions_thread = threading.Thread(target=self._listen_redis_actions)

    def start(self):
        """
        This method is used to start the sensors listener threads
        """
        self.redis_actions_thread.start()

    def _listen_redis_actions(self):
        """
        This method is used to listen to redis actions from the frontend
        """
        print("Listening to actions")
        pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe("actions")
        for message in pubsub.listen():
            data = json.loads(message["data"])

            match data["route"]:
                case "record:start":
                    if not self._is_recording:
                        self._start_recording()

                case "record:stop":
                    if self._is_recording:
                        self._stop_recording()

                case "record:pause":
                    self._pause_recording()

    def _start_recording(self):
        """
        This method is used to start recording the sensors data
        """
        print("Recording started")
        if self._is_paused and self._is_recording:
            self._is_paused = False
            return

        self._is_recording = True

        self.replay = ReplaySession.objects.create(
            start_time=timezone.now(),
        )
        self.replay.name = f"Replay session {self.replay.id}"
        self.replay.save()

    def _pause_recording(self):
        """
        This method is used to pause recording the sensors data
        """
        print("Recording paused")
        self._is_paused = True

    def _stop_recording(self):
        """
        This method is used to stop recording the sensors data
        """
        print("Recording stopped")
        self._is_recording = False
        self.replay.end_time = timezone.now()
        self.replay.save()
        self.replay = None


if __name__ == "__main__":
    sensors_listener = SensorsListener()
    sensors_listener.start()
