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
    }
)

django.setup()
import sys
sys.path.append('/app/backend')

from apps.replay import models