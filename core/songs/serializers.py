from rest_framework import serializers


class SongSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    album_id = serializers.CharField(source="album")
    release_date = serializers.DateField()
    genre = serializers.CharField()
