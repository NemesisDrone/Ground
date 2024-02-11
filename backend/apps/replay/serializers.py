from django.conf import settings
from rest_framework import serializers
from .models import ReplaySession, ReplaySessionData


class ReplaySessionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaySessionData
        fields = (
            "id",
            "index",
            "altitude",
            "latitude",
            "longitude",
            "speed",
            "roll",
            "pitch",
            "yaw",
        )
        read_only_fields = ("__all__",)


class ReplaySessionSerializer(serializers.ModelSerializer):
    data = ReplaySessionDataSerializer(many=True, read_only=True)

    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    @staticmethod
    def get_start_time(obj):
        return obj.start_time.timestamp()

    @staticmethod
    def get_end_time(obj):
        if obj.end_time is None:
            return 0
        return obj.end_time.timestamp()

    class Meta:
        model = ReplaySession
        fields = ("id", "start_time", "end_time", "name", "data")
        read_only_fields = ("id", "start_time", "end_time", "created_a", "updated_at")
        ordering = ["-created_at"]


class ReplaySessionListSerializer(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    @staticmethod
    def get_start_time(obj):
        return obj.start_time.timestamp()

    @staticmethod
    def get_end_time(obj):
        if obj.end_time is None:
            return 0
        return obj.end_time.timestamp()

    class Meta:
        model = ReplaySession
        fields = ("id", "start_time", "end_time", "name")
        read_only_fields = ("id", "start_time", "end_time", "created_at", "updated_at")
        ordering = ["-created_at"]
