from datetime import timedelta
import argparse
import django

django.setup()

"""
For every model we clear the database before populating it
"""


def add_user():
    """
    Create a first user in the database
    """
    from apps.user.models import User

    User.objects.all().delete()
    user = User.objects.create_user(identifier="Nemesis", password="nemesis")
    print('User Nemesis with password "nemesis" created')


def add_drone_settings():
    """
    Create a drone settings in the database
    """
    from apps.drone.models import DroneSettings, DroneModelSettings

    DroneSettings.objects.all().delete()
    DroneModelSettings.objects.all().delete()

    drone_settings = DroneSettings.objects.create(selected_drone_model=None)
    drone_model_settings = DroneModelSettings(
        name="Model 1", drone_settings=drone_settings
    )
    drone_model_settings.save()
    drone_settings.selected_drone_model = drone_model_settings
    drone_settings.save()

    print("Drone settings created")


def add_monitoring_images():
    """
    Create monitoring images
    """
    from apps.drone.models import DroneImage
    from django.core.files import File

    DroneImage.objects.all().delete()

    image = DroneImage()
    image.image.save("img1.jpg", File(open("/app/tmp/images/img1.jpg", "rb")))
    image.save()

    image = DroneImage()
    image.image.save("img2.jpg", File(open("/app/tmp/images/img2.jpg", "rb")))
    image.save()

    image = DroneImage()
    image.image.save("img3.jpg", File(open("/app/tmp/images/img3.jpg", "rb")))
    image.save()

    image = DroneImage()
    image.image.save("img4.jpg", File(open("/app/tmp/images/img4.jpg", "rb")))
    image.save()

    print("Monitoring images created")


def add_replay_session():
    """
    Create a replay session
    """
    from apps.replay.models import ReplaySession, ReplaySessionData
    from django.utils import timezone

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

    print("Creating replay session")
    for i in range(0, 136):
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
        # print(replay_data.index)

        if i % 5 == 0:
            if last_replay_data is not None:
                replay_data.altitude = last_replay_data.altitude + 1
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

    session.end_time = session_beginning + timedelta(seconds=13)
    session.name = "Test session"
    session.save()

    print("Replay session created")


parser = argparse.ArgumentParser(description="Populate the database with some data")
parser.add_argument("--all", action="store_true", help="Populate all the database")
parser.add_argument("--user", action="store_true", help="Populate the user table")
parser.add_argument(
    "--drone-settings", action="store_true", help="Populate the drone settings table"
)
parser.add_argument(
    "--monitoring", action="store_true", help="Populate the monitoring images table"
)
parser.add_argument(
    "--replay", action="store_true", help="Populate the replay session table"
)

args = parser.parse_args()

if (
    not args.all
    and not args.user
    and not args.drone_settings
    and not args.monitoring
    and not args.replay
):
    parser.print_help()

if args.all:
    add_replay_session()
    add_user()
    add_drone_settings()
    add_monitoring_images()

if args.user:
    add_user()

if args.drone_settings:
    add_drone_settings()

if args.monitoring:
    add_monitoring_images()

if args.replay:
    add_replay_session()


print("Done.")
