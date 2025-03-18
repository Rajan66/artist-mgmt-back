from rest_framework import serializers
from users.serializers import UserOutputSerializer


class ArtistSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user = UserOutputSerializer()
    name = serializers.CharField()
    first_release_year = serializers.IntegerField()
    no_of_albums_released = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateTimeField()
    gender = serializers.CharField()
    address = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField()


class AlbumArtistSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    first_release_year = serializers.IntegerField()
    no_of_albums_released = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateTimeField()
    gender = serializers.CharField()
    address = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField()
