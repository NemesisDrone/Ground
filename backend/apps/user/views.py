from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from ..user.models import User


class UserLoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_user_data(request: Request):
    """
    Get user data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def update_user_identifier(request: Request):
    """
    Update user identifier
    """
    user = request.user

    print(user)

    return Response(
        {
            "status": "success",
        }
    )
