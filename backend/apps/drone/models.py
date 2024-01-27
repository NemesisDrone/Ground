import json
import os
from django.db import models

from ..core.models import BaseModel


def default_canals():
    """
    This method is used to create the default canals for the drone
    :return: List of canals
    """
    return [{"canal": i, "gpios": []} for i in range(1, 11)]


class DroneModelSettings(BaseModel):
    # The name of the model (used on the drone)
    name = models.CharField(max_length=255)
    # Gpios used for each canal of servos
    servo_canals = models.JSONField(default=default_canals)
    # Gpios used for each canal of brushless motors
    brushless_canals = models.JSONField(default=default_canals)

    objects = models.Manager()

    drone_settings = models.ForeignKey(
        "DroneSettings", on_delete=models.CASCADE, related_name="models"
    )

    def get_config(self):
        """
        This method is used to get the config of the drone model as a payload to send to the drone
        :return: The config
        """
        return {
            "name": self.name,
            "servo_canals": self.servo_canals,
            "brushless_canals": self.brushless_canals,
        }

    def send_config_to_drone(self):
        """
        This method is used to send the config to the drone
        As to be called from django views/signal
        """
        if self.drone_settings.selected_drone_model != self:
            return

        import redis

        r = redis.Redis(
            host=os.environ.get("REDIS_HOST"),
            port=os.environ.get("REDIS_PORT"),
            decode_responses=True,
            db=0,
        )
        r.publish(
            "actions", json.dumps({"route": "config:data", "data": self.get_config()})
        )


class DroneSettings(BaseModel):
    selected_drone_model = models.ForeignKey(
        "DroneModelSettings",
        on_delete=models.CASCADE,
        related_name="drone_related_settings",
        null=True,
    )

    def get_current_config(self):
        """
        This method is used to get the config of the drone model as a payload to send to the drone
        :return: The config
        """
        if not self.selected_drone_model:
            return None

        return self.selected_drone_model.get_config()

    objects = models.Manager()


class DroneImage(BaseModel):
    image = models.ImageField(upload_to="drone_images/")

    objects = models.Manager()
