from django.db import models

from ..core.models import BaseModel


def default_canals():
    return [
        {
            "canal": 1,
            "gpios": [1,2]
        },
        {
            "canal": 2,
            "gpios": [3]
        },
        {
            "canal": 3,
            "gpios": [4]
        }
    ]


class DroneSettings(BaseModel):
    canals = models.JSONField(default=default_canals)


class DroneImage(BaseModel):
    image = models.ImageField(upload_to="drone_images/")