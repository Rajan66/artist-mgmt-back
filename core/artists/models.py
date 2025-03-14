from django.db import models
from users.models import CustomUser as User

from core.base.models import BaseModel, Profile


class Artist(BaseModel, Profile):
    user = models.OneToOneField(
        User,
        related_name="artist",
        on_delete=models.CASCADE,
    )
    name = models.CharField(unique=True, verbose_name="artist name")
    first_release_year = models.IntegerField(blank=True)
    no_of_albums_released = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Artist Profile"
        verbose_name_plural = "Artist Profiles"

    def __str__(self):
        return self.name
