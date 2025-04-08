import datetime

from albums.models.album import Album
from rest_framework.validators import ValidationError


def validate_release(id, release_date):
    album = Album.objects.filter(id=id).first()
    release_date_obj = datetime.datetime.strptime(release_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    if release_date_obj.year < album.release_date.year:
        raise ValidationError(
            "Song's release date cannot be less than Album's release date."
        )
