from albums.serializers.album import AlbumSerializer
from rest_framework import serializers


class SongSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    album = AlbumSerializer()
    release_date = serializers.DateField()
    genre = serializers.CharField()
