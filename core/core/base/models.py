import uuid

from django.db import models

from core.base.choices import GenderChoices


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile:
    dob = models.DateTimeField(blank=True, null=True)  # add proper validation for this
    gender = models.CharField(
        choices=GenderChoices,
        default=GenderChoices.MALE,
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
