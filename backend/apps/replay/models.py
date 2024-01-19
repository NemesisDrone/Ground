from django.db import models
from ..core.models import BaseModel


class ReplaySessionData(BaseModel):
    session = models.ForeignKey("ReplaySession", on_delete=models.CASCADE, related_name="data")

    # From timestamp in tenths of seconds
    index = models.IntegerField()

    altitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    speed = models.FloatField(null=True)

    roll = models.FloatField(null=True)
    pitch = models.FloatField(null=True)
    yaw = models.FloatField(null=True)

    objects = models.Manager()

    def __str__(self):
        return f"Session data : {self.index}"


class ReplaySession(BaseModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    name = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return f"Session : {self.start_time} to {self.end_time}"
