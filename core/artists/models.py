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
    manager = models.ForeignKey(
        User,
        related_name="manager",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    first_release_year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1980), max_value_current_year],
    )
    no_of_albums_released = models.PositiveIntegerField(default=0)
    profile_image = models.ImageField(
        upload_to="artists/profile", null=True, blank=True
    )
    cover_image = models.ImageField(upload_to="artists/cover", null=True, blank=True)

    class Meta:
        verbose_name = "Artist Profile"
        verbose_name_plural = "Artist Profiles"

    def __str__(self):
        return self.name
