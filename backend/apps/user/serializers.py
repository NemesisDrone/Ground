from rest_framework import serializers
from ..user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "identifier",
        )
        read_only_fields = ("id",)
