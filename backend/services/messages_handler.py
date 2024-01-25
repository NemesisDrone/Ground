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

    def _forward_message(self, message: Dict) -> None:
        """
        Forward a message to the frontend
        """
        payload = {"type": "communication.message", "message": message}

        async_to_sync(self.channel_layer.group_send)(self.group_name, payload)

    def _check_connection_status(self) -> None:
        """
        Check if the time since the last heartbeat is more than 3 seconds.
        If so, set the drone as disconnected
        """
        if time.time() - float(self.redis.get("LAST_HEARTBEAT_RECEIVED")) > 3 and int(
            self.redis.get("IS_DRONE_CONNECTED")
        ) == 1:
            self._forward_message(
                {
                    "type": "drone:connection-status",
                    "data": {"connected": False},
                }
            )
            self.redis.set("IS_DRONE_CONNECTED", 0)
            logging.critical("Drone disconnected")

    def _worker(self) -> None:
        logging.info("Starting communication forwarder")

        while True:
            message = None

            try:
                message = self.pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    data = json.loads(message["data"])
                    # Forward the message to the frontend
                    self._forward_message(data)

                # Check whether the drone is connected or not
                self._check_connection_status()

            except Exception as e:
                logging.error(f"Error while handling drone message: {e}.\nWith message: {message}")


if __name__ == "__main__":
    DroneMessagesHandler()