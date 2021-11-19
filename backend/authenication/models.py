import jwt

from datetime import datetime, timedelta

from django.conf import settings 
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, username: str, password: str = None):
        if username is None:
            raise TypeError("Users must have a at least username")

        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username: str, password: str):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_worker = True
        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=35, unique=True)
    name = models.CharField(max_length=35, null=True)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_worker = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username