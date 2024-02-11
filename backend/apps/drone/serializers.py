from django.conf import settings
from rest_framework import serializers
from .models import DroneSettings, DroneImage, DroneModelSettings


class DroneModelSettingsSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if self.instance is None:
            if DroneModelSettings.objects.filter(name=value).exists():
                raise serializers.ValidationError(
                    "A drone model with this name already exists"
                )
        else:
            if (
                DroneModelSettings.objects.filter(name=value)
                .exclude(id=self.instance.id)
                .exists()
            ):
                raise serializers.ValidationError(
                    "A drone model with this name already exists"
                )
        return value

    class Meta:
        model = DroneModelSettings
        fields = (
            "id",
            "name",
            "servo_canals",
            "brushless_canals",
            "drone_settings",
            "flight_mode_channel",
        )
        read_only_fields = ("id",)


class DroneSettingsSerializer(serializers.ModelSerializer):
    models = DroneModelSettingsSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["selected_drone_model"] = {
            "id": data["selected_drone_model"],
            "name": DroneModelSettings.objects.get(
                id=data["selected_drone_model"]
            ).name,
        }
        return data

    class Meta:
        model = DroneSettings
        fields = (
            "id",
            "models",
            "selected_drone_model",
        )
        read_only_fields = ("id", "models")


class DroneImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(method_name="get_image_url", read_only=True)

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
