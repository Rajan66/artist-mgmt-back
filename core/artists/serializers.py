from rest_framework import serializers
from users.models import CustomUser as User


class ArtistSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        User,
        queryset=User.objects.all(),
        many=False,
        read_only=False,
    )  # TODO change this to use raw query
    name = serializers.CharField()
    first_release_year = serializers.IntegerField()
    no_of_albums_released = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField(read_only=True)
