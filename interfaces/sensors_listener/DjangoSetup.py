import django
from django.conf import settings
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ.get("DB_DB"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
        }
    },
    INSTALLED_APPS=["apps.replay"],
    TIME_ZONE="Europe/Paris",
    USE_TZ=True,
    CHANNEL_LAYERS={
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(os.environ.get("REDIS_HOST"), os.environ.get("REDIS_PORT"))],
                "capacity": 3000,
                "expiry": 10,
            },
        },
    },
)

import sys

sys.path.append("../../backend")
django.setup()
