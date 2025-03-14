from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.base.choices import GenderChoices, RoleChoices
from core.base.models import BaseModel
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(_("email address"), unique=True)

    first_name = models.CharField(_("first name"), blank=True)
    last_name = models.CharField(_("last name"), blank=True)
    phone = models.CharField(
        _("phone"),
        unique=True,
        max_length=20,
        blank=True,
    )  # add validation

    gender = models.CharField(
        choices=GenderChoices,
        default=GenderChoices.MALE,
    )
    role = models.CharField(
        choices=RoleChoices,
        default=RoleChoices.ARTIST,
    )  # change to role table

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    dob = models.DateTimeField()  # add proper validation for this
    date_joined = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["dob", "gender"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
