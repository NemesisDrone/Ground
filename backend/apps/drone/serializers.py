from rest_framework import serializers
from .models import DroneSettings


class DroneSettingsSerializer(serializers.ModelSerializer):
    canals = serializers.JSONField()

    class Meta:
        model = DroneSettings
        fields = (
            "id",
            "canals",
        )
        read_only_fields = ("id",)