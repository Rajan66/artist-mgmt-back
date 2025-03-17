from django.db import models


class GenderChoices(models.TextChoices):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class RoleChoices(models.TextChoices):
    SUPER_ADMIN = "super_admin"
    ARTIST_MANAGER = "artist_manager"
    ARTIST = "artist"


class GenreChoices(models.TextChoices):
    RNB = "rnb"
    COUNTRY = "country"
    CLASSIC = "classic"
    ROCK = "rock"
    JAZZ = "jazz"


class AlbumChoices(models.TextChoices):
    SINGLE = "single"
    EP = "ep"
    ALBUM = "album"
