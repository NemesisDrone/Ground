import os
from typing import Dict
import redis
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class CommunicationLayer:
    """
    This class is used to handle messages from frontend
    """

    def __init__(self) -> None:

        self.redis = redis.StrictRedis(
            host=os.environ.get("REDIS_HOST"),
            port=os.environ.get("REDIS_PORT"),
            db=0,
            decode_responses=True,
        )
        # Messages from the drone
        self.ps_drone = self.redis.pubsub()
        self.ps_drone.subscribe("communication_forwarding")

        self.ps_frontend = self.redis.pubsub()
        self.ps_frontend.subscribe("actions")

        # Get the django channel layer. It is used to send messages to the frontend
        self.channel_layer = get_channel_layer()
        self.group_name = "communication"

    def send_to_frontend(self, message: Dict) -> None:
        """
        Send a message to the frontend
        """
        payload = {"type": "communication.message", "message": message}
        async_to_sync(self.channel_layer.group_send)(self.group_name, payload)
