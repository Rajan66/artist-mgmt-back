from django.core.validators import MinValueValidator
from django.db import models
from users.models.user import CustomUser as User

from artists.utils import current_year, max_value_current_year
from core.base.models import Profile


class Artist(Profile):
    user = models.OneToOneField(
        User,
        related_name="artist",
        on_delete=models.CASCADE,
    )
    name = models.CharField(blank=True, null=True, verbose_name="artist name")
    # no use, we have to validate in the services anyways
    first_release_year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1980), max_value_current_year],
    )
    no_of_albums_released = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Artist Profile"
        verbose_name_plural = "Artist Profiles"

    def __str__(self):
        return self.name
