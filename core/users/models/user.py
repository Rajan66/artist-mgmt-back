from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.managers import CustomUserManager

from core.base.choices import RoleChoices
from core.base.models import BaseModel


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(
        choices=RoleChoices,
        default=RoleChoices.ARTIST,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
