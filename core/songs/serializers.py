from rest_framework import serializers


class SongSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    album_name = serializers.CharField()
    genre = serializers.CharField()
