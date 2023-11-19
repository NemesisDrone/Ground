import json
from channels.generic.websocket import AsyncWebsocketConsumer
import redis.asyncio as redis
from django.conf import settings
from .utils import get_user


class CommunicationConsumer(AsyncWebsocketConsumer):
    """
    This consumer handles the communication between the frontend and the backend. And
    """

    async def connect(self):
        user = await get_user(self.scope)

        # If the user is not authenticated, close the connection.
        if user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add("communication", self.channel_name)
        self.redis = await redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("communication", self.channel_name)

    async def receive(self, text_data):
        """
        This method is called when the consumer receives a message from the frontend.
        It will then send the message to redis.
        """
        print(text_data)
        await self.redis.publish("actions", text_data)

    async def communication_message(self, event):
        """
        Receive message from redis interfaces, and send it to the frontend.
        """
        await self.send(text_data=json.dumps(event["message"]))
