# from albums.selectors import fetch_album
from rest_framework import status

from core.utils.response import error_response, success_response

# from songs.serializers import SongSerializer


class SongService:
    def get_songs(self):
        try:
            # songs_dicts = fetch_songs()
            # for album in songs_dicts:
            #     album_id = album.get("artist_id")
            #     album_dict = fetch_album(id=album_id)
            #
            #     serializer = SongSerializer(album_dict)
            #     album["artist"] = serializer.data
            #
            # serializer = SongSerializer(songs_dicts, many=True)
            # songs = serializer.data

            return success_response(
                # data=songs,
                message="Songs retrieved successfully",
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch songs",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_song(self, id):
        pass

    def create(self, payload):
        pass

    def update(self, payload):
        pass

    def delete(self, payload):
        pass
