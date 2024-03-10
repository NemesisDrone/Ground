import json
from typing import Dict

from channels.layers import get_channel_layer
import redis
import os
import sys
import django
from asgiref.sync import async_to_sync
import logging
import time

"""
Setup django environment
Add root application to the path.
It is used for the script to be able to import the django settings.
It is necessary because channels required it.
"""
sys.path.append("../")
sys.path.append("./")
django.setup()

from apps.drone.models import DroneSettings

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


class DroneMessagesHandler:
    """
    This class is used for multiple purposes:
    - Forward messages to the frontend
    - Answer to drone messages
    - Handle connection status
    - Answer to heartbeat

    """

    def __init__(self) -> None:
        self.redis = redis.Redis(
            host=os.environ.get("REDIS_HOST"),
            port=os.environ.get("REDIS_PORT"),
            decode_responses=True,
            db=0,
        )
        # Get the django channel layer. It is used to send messages to the frontend
        self.channel_layer = get_channel_layer()
        self.group_name = "communication"
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe("communication_forwarding")

        self._worker()

    def _send_to_frontend(self, message: Dict) -> None:
        """
        Send a message to the frontend
        """
        payload = {"type": "communication.message", "message": message}

        async_to_sync(self.channel_layer.group_send)(self.group_name, payload)

    def _send_to_drone(self, message: Dict) -> None:
        """
        Send a message to the drone
        """
        self.redis.publish("actions", json.dumps(message))

    def _check_connection_status(self) -> None:
        """
        Check if the time since the last heartbeat is more than 3 seconds.
        If so, set the drone as disconnected
        """
        if (
            time.time() - float(self.redis.get("LAST_HEARTBEAT_RECEIVED")) > 3
            and int(self.redis.get("IS_DRONE_CONNECTED")) == 1
        ):
            self._send_to_frontend(
                {
                    "type": "drone:connection-status",
                    "data": {"connected": False},
                }
            )
            self.redis.set("IS_DRONE_CONNECTED", 0)
            logging.critical("Drone disconnected")

    def _send_config(self) -> None:
        """
        Send the config to the drone
        """
        config = DroneSettings.objects.get().get_current_config()
        self._send_to_drone({"route": "config:data", "data": config})
        print("Sending config to drone")

    def _send_objectives(self) -> None:
        """
        Send the objectives to the drone
        """
        objectives = DroneSettings.objects.get().get_objectives()
        self._send_to_drone({"route": "config:objectives", "data": objectives})

    def _handle_message_answer(self, message: Dict) -> None:
        """
        Handle the message answer
        """
        match message["type"]:
            case "config:get":
                self._send_config()
            case "config:objectives:get":
                self._send_objectives()

    def _worker(self) -> None:
        logging.info("Starting communication forwarder")

        while True:
            message = None

            try:
                message = self.pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    data = json.loads(message["data"])
                    # Forward the message to the frontend
                    self._send_to_frontend(data)
                    # Handle the message answer
                    self._handle_message_answer(data)

                # Check whether the drone is connected or not
                self._check_connection_status()

            except Exception as e:
                logging.error(
                    f"Error while handling drone message: {e}.\nWith message: {message}"
                )


if __name__ == "__main__":
    DroneMessagesHandler()
