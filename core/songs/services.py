from rest_framework import status

from core.utils.response import error_response, success_response
from songs.selectors import fetch_songs
from songs.serializers import SongSerializer


class SongService:
    def get_songs(self):
        try:
            songs_dicts = fetch_songs()
            serializer = SongSerializer(songs_dicts, many=True)
            songs = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch songs",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=songs,
            message="Songs retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_song(self, id):
        pass

    def create(self, payload):
        pass

    def update(self, payload):
        pass

    def delete(self, payload):
        pass
