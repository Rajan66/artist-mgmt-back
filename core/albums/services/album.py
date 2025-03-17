from albums.selectors import fetch_albums
from albums.serializers.album import AlbumSerializer
from artists.selectors import fetch_artist
from artists.serializers import ArtistSerializer
from rest_framework import status
from users.selectors import fetch_user
from users.serializers import UserOutputSerializer

from core.utils.response import error_response, success_response


class AlbumService:
    def get_albums(self):
        try:
            albums_dicts = fetch_albums()
            for album in albums_dicts:
                artist_id = album.get("artist_id")
                artist_dict = fetch_artist(id=artist_id)

                user_dict = fetch_user(artist_dict)

                serializer = UserOutputSerializer(user_dict)
                artist_dict["user"] = serializer.data

                serializer = ArtistSerializer(artist_dict)
                album["artist"] = serializer.data

            serializer = AlbumSerializer(albums_dicts, many=True)
            albums = serializer.data

            return success_response(
                data=albums,
                message="Albums retrieved successfully",
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch albums",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
