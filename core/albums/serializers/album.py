from artists.serializers import AlbumArtistSerializer
from rest_framework import serializers


class BaseAlbumSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    total_tracks = serializers.IntegerField()
    release_date = serializers.DateField()
    album_type = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class AlbumSerializer(BaseAlbumSerializer, serializers.Serializer):
    artist = AlbumArtistSerializer()
    cover_image = serializers.ImageField()


class AlbumOutputSerializer(BaseAlbumSerializer, serializers.Serializer):
    artist = AlbumArtistSerializer()
    cover_image = serializers.CharField()


class AlbumFetchSerializer(BaseAlbumSerializer, serializers.Serializer):
    artist_id = serializers.UUIDField()
    cover_image = serializers.CharField()
