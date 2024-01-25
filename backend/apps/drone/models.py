from django.db import models

from ..core.models import BaseModel


def default_canals():
    """
    This method is used to create the default canals for the drone
    :return: List of canals
    """
    return [
        {
            "canal": i,
            "gpios": []
        } for i in range(1, 11)
    ]


class DroneModelSettings(BaseModel):
    # The name of the model (used on the drone)
    name = models.CharField(max_length=255)
    # Gpios used for each canal of servos
    servo_canals = models.JSONField(default=default_canals)
    # Gpios used for each canal of brushless motors
    brushless_canals = models.JSONField(default=default_canals)

    objects = models.Manager()

    drone_settings = models.ForeignKey("DroneSettings", on_delete=models.CASCADE, related_name="models")


class DroneSettings(BaseModel):
    selected_drone_model = models.ForeignKey("DroneModelSettings", on_delete=models.CASCADE, related_name="drone_related_settings", null=True)

    objects = models.Manager()


class DroneImage(BaseModel):
    image = models.ImageField(upload_to="drone_images/")

    objects = models.Manager()