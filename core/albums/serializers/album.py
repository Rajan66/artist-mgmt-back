from artists.serializers import ArtistSerializer
from rest_framework import serializers


class AlbumSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    artist = ArtistSerializer()
    cover_image = serializers.ImageField()
    total_tracks = serializers.IntegerField()
    release_date = serializers.DateField()
    type = serializers.CharField()
