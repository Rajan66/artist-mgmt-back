import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.base.choices import GenderChoices


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(BaseModel):
    first_name = models.CharField(_("first name"), blank=True)
    last_name = models.CharField(_("last name"), blank=True)
    dob = models.DateTimeField(blank=True, null=True)  # add proper validation for this
    gender = models.CharField(
        choices=GenderChoices,
        null=True,
        blank=False,
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
