"""
This script is only used temporarily to test the communication between the backend and the frontend.
"""
from channels.layers import get_channel_layer
import asyncio
import random
import time


async def send(sensor_data):
    channel_layer = get_channel_layer()
    group_name = "communication"  # Replace with the actual group name if applicable
    message = {
        "type": "communication.message",
        "message": sensor_data,
    }
    await channel_layer.group_send(group_name, message)

while True:
    rand = random.randint(95, 104)
    sensor_data = {
        "type": "sensors:altitude",
        "data": rand
    }
    asyncio.run(send(sensor_data))
    print(f'altitude {rand}')
    time.sleep(.33)
    rand = random.randint(0, 100)
    sensor_data = {
        "type": "sensors:battery",
        "data": rand
    }
    asyncio.run(send(sensor_data))
    print(f'battery {rand}')
    time.sleep(.33)
    rand = random.randint(35, 43)
    sensor_data = {
        "type": "sensors:speed",
        "data": rand
    }
    asyncio.run(send(sensor_data))
    print(f'speed {rand}')
    time.sleep(.33)

    rand = random.randint(0, 4)
    sensor_data = {
        "type": "log",
        "data": {
            "time": time.strftime("%H:%M:%S", time.localtime()),
        }
    }
    match rand:
        case 0:
            sensor_data["data"]["level"] = "DEBUG"
            sensor_data["data"]["message"] = "This is a debug message"
        case 1:
            sensor_data["data"]["level"] = "INFO"
            sensor_data["data"]["message"] = "That's ok, This is an info message"
        case 2:
            sensor_data["data"]["level"] = "WARNING"
            sensor_data["data"]["message"] = "Achtung, this is a warning message"
        case 3:
            sensor_data["data"]["level"] = "ERROR"
            sensor_data["data"]["message"] = "Ah ptn, this is an error message"
        case 4:
            sensor_data["data"]["level"] = "CRITICAL"
            sensor_data["data"]["message"] = "C la d This is a critical message"

    if random.randint(0, 4) == 0:
        sensor_data["data"]["message"] = "This is a reallt big message because it has to be tested. Indeed a big message can broke an Ui"

    asyncio.run(send(sensor_data))
