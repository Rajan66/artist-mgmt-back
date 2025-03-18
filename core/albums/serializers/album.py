from artists.serializers import AlbumArtistSerializer
from rest_framework import serializers


class AlbumSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    artist = AlbumArtistSerializer()
    cover_image = serializers.ImageField()
    total_tracks = serializers.IntegerField()
    release_date = serializers.DateField()
    album_type = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class AlbumFetchSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    artist_id = serializers.UUIDField()
    cover_image = serializers.ImageField()
    total_tracks = serializers.IntegerField()
    release_date = serializers.DateField()
    album_type = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
