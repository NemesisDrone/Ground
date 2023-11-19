import rest_framework_simplejwt.exceptions
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from channels.db import database_sync_to_async
from ..user.models import User
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(scope) -> User:
    """
    This function take a django channel scope and return a user object.
    It will return an AnonymousUser if the user is not authenticated.
    """
    access = scope["cookies"]["access"]
    refresh = scope["cookies"]["refresh"]

    try:
        user = User.objects.get(
            id=AccessToken(access)["user_id"]
        )
    # TODO: Handle refresh token
    # except rest_framework_simplejwt.exceptions.TokenError:
    #     #     Refresh token

    except User.objects.DoesNotExist:
        user = AnonymousUser()

    return user
