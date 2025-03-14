from django.db import models

from core.base.choices import GenreChoices
from core.base.models import BaseModel


class Song(BaseModel):
    title = models.CharField(max_length=255)
    album_name = models.CharField(max_length=255)
    genre = models.CharField(choices=GenreChoices)

    def __str__(self):
        return self.title + " " + self.album_name
