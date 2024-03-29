from datetime import timedelta
import django
import argparse

parser = argparse.ArgumentParser(description="Create a big replay session.")
parser.add_argument(
    "--nb", type=int, default=136, help="Number of replay_data to create"
)
parser.add_argument(
    "--name", type=str, default="Test big session", help="Name of the session"
)
parser.add_argument(
    "--clear", action="store_true", help="Clear the database before populating it"
)

args = parser.parse_args()

django.setup()


"""
Create a replay session
"""
from apps.replay.models import ReplaySession, ReplaySessionData
from django.utils import timezone

if args.clear:
    ReplaySession.objects.all().delete()
    ReplaySessionData.objects.all().delete()


session = ReplaySession(
    start_time=timezone.now(),
)
session.save()

session_beginning = timezone.now()

last_replay_data = None
speed_factor = 1
pitch_factor = 1
roll_factor = 1
yaw_factor = 1


for i in range(0, args.nb):
    replay_data = ReplaySessionData(
        session=session,
        index=i * 10,
        latitude=-0.7563779,
        longitude=48.0879123,
        altitude=100,
        speed=0,
        roll=0,
        pitch=0,
        yaw=0,
    )
    print(replay_data.index)

    if i % 5 == 0:
        if last_replay_data is not None:
            replay_data.altitude = last_replay_data.altitude + 1

            if replay_data.altitude > 130:
                replay_data.altitude = 100
        else:
            replay_data.altitude = 100

        if last_replay_data is not None:
            replay_data.latitude = last_replay_data.latitude + 0.0001
        else:
            replay_data.latitude = -0.7563779

    else:
        if last_replay_data is not None:
            replay_data.altitude = last_replay_data.altitude
        else:
            replay_data.altitude = 100

        if last_replay_data is not None:
            replay_data.latitude = last_replay_data.latitude
        else:
            replay_data.latitude = -0.7563779

    if i % 7 == 0:
        if last_replay_data is not None:
            replay_data.speed = last_replay_data.speed + 2
            if replay_data.speed > 34:
                replay_data.speed = 20
                speed_factor = -1

            if replay_data.speed < 12 and speed_factor == -1:
                replay_data.speed = 12
                speed_factor = 1
        else:
            replay_data.speed = 0
    else:
        if last_replay_data is not None:
            replay_data.speed = last_replay_data.speed
        else:
            replay_data.speed = 0

    if i % 3 == 0:
        if last_replay_data is not None:
            replay_data.pitch = last_replay_data.pitch + 2
            if replay_data.pitch > 34:
                replay_data.pitch = 20
                pitch_factor = -1

            if replay_data.pitch < 12 and pitch_factor == -1:
                replay_data.pitch = 12
                pitch_factor = 1

            replay_data.roll = last_replay_data.roll + 2
            if replay_data.roll > 34:
                replay_data.roll = 20
                roll_factor = -1

            if replay_data.roll < 12 and roll_factor == -1:
                replay_data.roll = 12
                roll_factor = 1

            replay_data.yaw = last_replay_data.yaw + 2
            if replay_data.yaw > 34:
                replay_data.yaw = 20
                yaw_factor = -1

            if replay_data.yaw < 12 and yaw_factor == -1:
                replay_data.yaw = 12
                yaw_factor = 1
        else:
            replay_data.pitch = 0
            replay_data.roll = 0
            replay_data.yaw = 0
    else:
        if last_replay_data is not None:
            replay_data.pitch = last_replay_data.pitch
            replay_data.roll = last_replay_data.roll
            replay_data.yaw = last_replay_data.yaw
        else:
            replay_data.pitch = 0
            replay_data.roll = 0
            replay_data.yaw = 0

    last_replay_data = replay_data
    replay_data.save()

session.end_time = session_beginning + timedelta(seconds=args.nb / 10)
session.name = args.name
session.save()


print("DB populated")
