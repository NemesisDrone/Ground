import django
from django.conf import settings
import os

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

INSTALLED_APPS = []


django.setup()