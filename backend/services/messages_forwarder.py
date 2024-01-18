import json
from channels.layers import get_channel_layer
import redis
import os
import sys
import django
from asgiref.sync import async_to_sync
import logging
import time

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

r = redis.Redis(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    decode_responses=True,
    db=0,
)

"""
Add root application to the path.
It is used for the script to be able to import the django settings.
It is necessary because channels required it.
"""
sys.path.append("../")
sys.path.append("./")
django.setup()
channel_layer = get_channel_layer()
group_name = "communication"


pubsub = r.pubsub()
pubsub.subscribe("communication_forwarding")

logging.info("Starting communication forwarder")
while True:
    try:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            data = json.loads(message["data"])

            payload = {"type": "communication.message", "message": data}

            async_to_sync(channel_layer.group_send)(group_name, payload)

        """
        If time since last heartbeat is more than 3 seconds, set the drone as disconnected
        """
        if ((time.time() - float(r.get("LAST_HEARTBEAT_RECEIVED"))) > 3) and int(
            r.get("IS_DRONE_CONNECTED")
        ) == 1:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "communication.message",
                    "message": {
                        "type": "drone:connection-status",
                        "data": {"connected": False},
                    },
                },
            )
            r.set("IS_DRONE_CONNECTED", 0)
            logging.critical("Drone disconnected")

    except Exception as e:
        logging.error("Error: %s", e)
