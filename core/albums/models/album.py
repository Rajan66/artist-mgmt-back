from artists.models import Artist
from django.db import models

from core.base.choices import AlbumChoices
from core.base.models import BaseModel


class Album(BaseModel):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, related_name="albums", on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to="albums/", null=True, blank=True)
    total_tracks = models.PositiveIntegerField(default=0)
    release_date = models.DateField()
    album_type = models.CharField(choices=AlbumChoices, default=AlbumChoices.SINGLE)

    def __str__(self):
        return self.title
