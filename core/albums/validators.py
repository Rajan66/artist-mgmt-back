import datetime

from artists.models import Artist
from rest_framework.validators import ValidationError


def validate_release(id, release_date):
    artist = Artist.objects.filter(id=id).first()
    release_date_obj = datetime.datetime.strptime(release_date, "%m/%d/%Y")

    if release_date_obj.year < artist.first_release_year:
        raise ValidationError("Release date cannot be less than debut year.")
