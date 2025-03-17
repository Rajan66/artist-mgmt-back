from django.db import connection
from rest_framework import status
from users.selectors import fetch_user
from users.serializers import UserOutputSerializer

from artists.selectors import fetch_artists
from artists.serializers import ArtistSerializer
from core.utils.response import error_response, success_response


class ArtistService:
    def get_artists(self):
        try:
            artist_dicts = fetch_artists()

            for artist in artist_dicts:
                user_dicts = fetch_user(artist)
                serializer = UserOutputSerializer(user_dicts)
                artist["user"] = serializer.data

            serializer = ArtistSerializer(artist_dicts, many=True)
            artists = serializer.data

            return success_response(
                data=artists,
                message="Artists retrieved successfully",
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Artist retrieval failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_artist(self, id):
        try:
            with connection.cursor() as c:
                c.execute("SELECT * FROM artists_artist;")
                results = c.fetchall()

                columns = []
                for col in c.description:
                    columns.append(col[0])

                artist_dicts = [dict(zip(columns, row)) for row in results]

                for artist in artist_dicts:
                    user_id = artist.get("user_id")
                    # TODO move raw query code to selectors
                    c.execute("SELECT * FROM users_customuser WHERE id=%s", [user_id])
                    result = c.fetchone()

                    if not result:
                        return error_response(
                            error="Invalid user ID",
                            message="User not found",
                            status=status.HTTP_404_NOT_FOUND,
                        )

                    columns = [col[0] for col in c.description]
                    user_dicts = dict(zip(columns, result))
                    serializer = UserOutputSerializer(user_dicts)
                    artist["user"] = serializer.data

            serializer = ArtistSerializer(artist_dicts, many=True)
            artists = serializer.data

            return success_response(
                data=artists,
                message="Artists retrieved successfully",
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Artist retrieval failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
