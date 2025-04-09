from albums.models.album import Album
from dateutil import parser
from rest_framework.validators import ValidationError


def validate_release(id, release_date):
    release_date_obj = parser.isoparse(release_date)
    release_date_only = release_date_obj.date()
    album = Album.objects.filter(id=id).first()

    if release_date_only.year < album.release_date.year:
        raise ValidationError(
            "Song's release date cannot be less than Album's release date."
        )
