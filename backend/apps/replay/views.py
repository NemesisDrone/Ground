from rest_framework import viewsets, permissions
from .serializers import (
    ReplaySessionSerializer,
    ReplaySessionDataSerializer,
    ReplaySessionListSerializer,
)

from .models import ReplaySession, ReplaySessionData


class ReplaySessionViewset(viewsets.ModelViewSet):
    """
    This viewset is used to list all the replay sessions, update or delete them.
    """

    queryset = ReplaySession.objects.all().order_by("-created_at")
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ReplaySessionListSerializer
        return ReplaySessionSerializer
