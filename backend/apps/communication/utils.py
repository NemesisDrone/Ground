import rest_framework_simplejwt.exceptions
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from channels.db import database_sync_to_async
from ..user.models import User
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist


@database_sync_to_async
def get_user(scope) -> User:
    """
    This function take a django channel scope and return a user object.
    It will return an AnonymousUser if the user is not authenticated.
    """
    access = scope["cookies"]["access"]
    refresh = scope["cookies"]["refresh"]

    try:
        user = User.objects.get(id=AccessToken(access)["user_id"])
    # Handle jwt token auto refreshing
    except rest_framework_simplejwt.exceptions.TokenError:
        try:
            return User.objects.get(id=RefreshToken(refresh)["user_id"])
        except rest_framework_simplejwt.exceptions.TokenError:
            user = AnonymousUser()

    except ObjectDoesNotExist:
        user = AnonymousUser()

    return user
