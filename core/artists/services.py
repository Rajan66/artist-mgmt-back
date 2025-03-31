import uuid

from django.db import DatabaseError, connection
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from users.models.user import CustomUser as User
from users.selectors import fetch_user
from users.serializers import UserOutputSerializer

from artists.models import Artist
from artists.selectors import fetch_artists
from artists.serializers import ArtistSerializer
from core.utils.exceptions import CustomAPIException
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
                c.execute("SELECT * FROM artists_artist WHERE id=%s", [id])
                result = c.fetchone()

                if not result:
                    raise ValueError("Invalid artist ID")

                columns = []
                for col in c.description:
                    columns.append(col[0])

                artist_dict = dict(zip(columns, result))
                user_id = artist_dict.get("user_id")

                c.execute(
                    "SELECT * FROM users_customuser WHERE id=%s",
                    [user_id],
                )
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
                artist_dict["user"] = serializer.data

            serializer = ArtistSerializer(artist_dict)
            artist = serializer.data

            return success_response(
                data=artist,
                message="Artist retrieved successfully",
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            raise CustomAPIException(
                error=str(e),
                detail="Invalid ID",
                code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return error_response(
                error=str(e),
                message="Artist retrieval failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, payload, user_id):
        try:
            payload = payload or {}
            id = payload.get("id", uuid.uuid4())
            manager_id = payload.get("manager_id", None)
            name = payload.get("name", "")
            first_release_year = payload.get("first_release_year", 0)
            no_of_albums_released = payload.get("no_of_albums_released", 0)
            first_name = payload.get("first_name", "")
            last_name = payload.get("last_name", "")
            dob = payload.get("dob", None)
            gender = payload.get("gender", None)
            address = payload.get("address", "")
            created_at = payload.get("created_at", timezone.now())
            updated_at = timezone.now()

            if manager_id:
                check_manager = User.objects.filter(
                    id=manager_id, role="artist_manager"
                ).exists()
                if not check_manager:
                    raise ValidationError(
                        "Invalid manager ID or the user is not a manager."
                    )
            with connection.cursor() as c:
                c.execute(
                    """INSERT INTO artists_artist (id,manager_id, name, first_release_year, no_of_albums_released, first_name, last_name, dob, gender, address,  created_at, updated_at, user_id)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
                    """,
                    [
                        id,
                        manager_id,
                        name,
                        first_release_year,
                        no_of_albums_released,
                        first_name,
                        last_name,
                        dob,
                        gender,
                        address,
                        created_at,
                        updated_at,
                        user_id,
                    ],
                )
                result = c.fetchone()
                if not result:
                    raise Exception(
                        "Artist profile creation failed"
                    )  # TODO CustomException, or try to send status from here

                columns = []
                for col in c.description:
                    columns.append(col[0])

            artist_dicts = dict(zip(columns, result))
            print(artist_dicts)

            user_dicts = fetch_user(artist_dicts)
            serializer = UserOutputSerializer(user_dicts)
            artist_dicts["user"] = serializer.data

            serializer = ArtistSerializer(artist_dicts)
            artist_profile = serializer.data

            return success_response(
                data=artist_profile,
                message="Artist profile created succesfully",
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            print(str(e))
            return error_response(
                error=str(e),
                message="Failed to create artist profile",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            print(str(e))
            return error_response(
                error=str(e),
                message="Failed to create artist profile",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, payload, id):
        try:
            with connection.cursor() as c:
                c.execute(
                    "SELECT * FROM artists_artist WHERE id=%s",
                    [id],
                )
                result = c.fetchone()
                if not result:
                    raise Exception("Artist not found")

                columns = []
                for col in c.description:
                    columns.append(col[0])

                artist_profile = dict(zip(columns, result))
                name = payload.get("name", artist_profile.get("name"))
                first_release_year = payload.get(
                    "first_release_year", artist_profile.get("first_release_year")
                )
                no_of_albums_released = payload.get(
                    "no_of_albums_released", artist_profile.get("no_of_albums_released")
                )
                first_name = payload.get("first_name", artist_profile.get("first_name"))
                last_name = payload.get("last_name", artist_profile.get("last_name"))
                dob = payload.get("dob", artist_profile.get("dob"))
                gender = payload.get("gender", artist_profile.get("gender"))
                address = payload.get("address", artist_profile.get("address"))
                updated_at = timezone.now()

                c.execute(
                    """UPDATE artists_artist SET
                    name=%s, first_release_year=%s, no_of_albums_released=%s, first_name=%s, last_name=%s, dob=%s, gender=%s, address=%s,  updated_at=%s 
                    WHERE id=%s RETURNING *;
                    """,
                    [
                        name,
                        first_release_year,
                        no_of_albums_released,
                        first_name,
                        last_name,
                        dob,
                        gender,
                        address,
                        updated_at,
                        id,
                    ],
                )
                result = c.fetchone()
                if not result:
                    raise Exception("Failed to update the artist")

                columns = []
                for col in c.description:
                    columns.append(col[0])

            artist_dict = dict(zip(columns, result))

            user_dict = fetch_user(artist_dict)
            serializer = UserOutputSerializer(user_dict)
            artist_dict["user"] = serializer.data

            serializer = ArtistSerializer(artist_dict)
            profile = serializer.data

            return success_response(
                profile,
                message="Artist profile updated succesfully",
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="User profile updation failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, id):
        try:
            with connection.cursor() as c:
                c.execute(
                    "DELETE FROM artists_artist WHERE id=%s RETURNING TRUE;",
                    [id],
                )
                result = c.fetchone()

                if not result:
                    return error_response(
                        error="Invalid artist ID",
                        message="Artist does not exist",
                        status=status.HTTP_404_NOT_FOUND,
                    )

            return success_response(
                message="Artist deleted successfully",
                status=status.HTTP_204_NO_CONTENT,
            )

        except DatabaseError as e:
            return error_response(
                error=str(e),
                message="Database error",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_manager_artists(self, manager_id):
        try:
            filtered_artists = Artist.objects.filter(manager=manager_id)

            artists = ArtistSerializer(filtered_artists, many=True).data

            return success_response(
                data=artists,
                message="Artists retrieved successfully",
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch artists",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
