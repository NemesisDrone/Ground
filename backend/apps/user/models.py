from ..core.models import BaseModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, BaseModel):
    identifier = models.CharField(
        db_index=True,
        unique=True,
    )
    USERNAME_FIELD = "identifier"
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.identifier

