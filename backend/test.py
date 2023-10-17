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
        "type": "sensors.altitude",
        "data": rand
    }
    asyncio.run(send(sensor_data))
    print(f'altitude {rand}')
    time.sleep(.33)
    rand = random.randint(0, 100)
    sensor_data = {
        "type": "sensors.battery",
        "data": rand
    }
    asyncio.run(send(sensor_data))
    print(f'battery {rand}')
    time.sleep(.33)
    rand = random.randint(35, 43)
    sensor_data = {
        "type": "sensors.speed",
        "data": rand
    }
    asyncio.run(send(sensor_data))
    print(f'speed {rand}')
    time.sleep(.33)