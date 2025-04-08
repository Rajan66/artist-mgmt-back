from rest_framework import serializers
from songs.serializers import SongOutputSerializer


class RecentSongSerializer(serializers.Serializer):
    song = SongOutputSerializer()
