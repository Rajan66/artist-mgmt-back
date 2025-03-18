from django.contrib import admin

from albums.models.album import Album
from albums.models.song import Song

admin.site.register(Song)
admin.site.register(Album)
