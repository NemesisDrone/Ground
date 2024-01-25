from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import DroneSettingsSerializer, DroneImageSerializer, DroneModelSettingsSerializer

from .models import DroneSettings, DroneImage, DroneModelSettings


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_drone_settings(request: Request):
    """
    Get drone settings
    """
    drone_settings = DroneSettings.objects.first()
    serializer = DroneSettingsSerializer(drone_settings)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def update_selected_drone_settings_model(request: Request):
    """
    Update the selected drone settings model
    """
    drone_settings = DroneSettings.objects.first()

    serializer = DroneSettingsSerializer(drone_settings, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


class DroneSettingsModelViewSet(viewsets.ModelViewSet):
    """
    This viewset is used to list all the drone settings model, and to create new ones or delete/update them.
    """
    queryset = DroneModelSettings.objects.all().order_by('-created_at')
    serializer_class = DroneModelSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]


class DroneImagesViewSet(viewsets.ModelViewSet):
    """
    This viewset is used to list all the drone images, and to create new ones or delete them.
    """
    queryset = DroneImage.objects.all().order_by('-created_at')
    serializer_class = DroneImageSerializer
    permission_classes = [permissions.IsAuthenticated]
