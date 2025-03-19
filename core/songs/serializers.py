from rest_framework import serializers


class BaseSongSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    release_date = serializers.DateField()
    genre = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class SongSerializer(BaseSongSerializer, serializers.Serializer):
    album_id = serializers.CharField(source="album")


class SongOutputSerializer(BaseSongSerializer, serializers.Serializer):
    artist_id = serializers.CharField()
    album_id = serializers.CharField(source="album")
