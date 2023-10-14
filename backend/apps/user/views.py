from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

class UserLoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)