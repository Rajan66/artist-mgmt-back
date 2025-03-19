from rest_framework import status

from core.utils.response import error_response, success_response
from songs.selectors import (
    fetch_album_songs,
    fetch_artist_songs,
    fetch_song,
    fetch_songs,
)
from songs.serializers import SongOutputSerializer, SongSerializer


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
        try:
            song_dict = fetch_song(id=id)
            serializer = SongSerializer(song_dict)
            song = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch song",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=song,
            message="Song retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_album_songs(self, album_id):
        try:
            songs_dicts = fetch_album_songs(album_id=album_id)
            serializer = SongSerializer(songs_dicts, many=True)
            songs = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch album's songs",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=songs,
            message="Songs retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_artist_songs(self, artist_id):
        try:
            song_dicts = fetch_artist_songs(artist_id=artist_id)
            serializer = SongOutputSerializer(song_dicts, many=True)
            song = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch song",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=song,
            message="Song retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def create(self, payload):
        pass

    def update(self, payload):
        pass

    def delete(self, payload):
        pass
