from django.conf import settings
from rest_framework import serializers
from .models import DroneSettings, DroneImage


class DroneSettingsSerializer(serializers.ModelSerializer):
    canals = serializers.JSONField()

    class Meta:
        model = DroneSettings
        fields = (
            "id",
            "canals",
        )
        read_only_fields = ("id",)


class DroneImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(
        method_name="get_image_url", read_only=True
    )

    @staticmethod
    def get_image_url(obj):
        return settings.BACKEND_URL + obj.image.url

    class Meta:
        model = DroneImage
        fields = (
            "id",
            "url",
        )
        read_only_fields = ("id",)
        ordering = ["-created_at"]