from django.db import models

from core.base.models import BaseModel


class TokenBlacklist(BaseModel):
    token = models.CharField()
