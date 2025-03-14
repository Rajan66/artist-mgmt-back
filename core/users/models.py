from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.base.choices import RoleChoices
from core.base.models import BaseModel, Profile
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(
        choices=RoleChoices,
        default=RoleChoices.ARTIST,
    )
    date_joined = models.DateTimeField(default=timezone.now)
    is_removed = models.BooleanField(default=False)
    created_at = None
    is_staff = None
    is_active = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(Profile):
    user = models.OneToOneField(
        CustomUser,
        related_name="user",
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(_("first name"), blank=True)
    last_name = models.CharField(_("last name"), blank=True)

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )  # add validation

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        return self.user.email
