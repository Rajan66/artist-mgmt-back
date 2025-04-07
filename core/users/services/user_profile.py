import uuid

from django.db import DatabaseError, connection
from django.utils import timezone
from rest_framework import status
from users.models.user_profile import UserProfile
from users.selectors import fetch_user, fetch_user_profiles
from users.serializers import (
    UserOutputSerializer,
    UserProfileOutputSerializer,
    UserProfileSerializer,
    UserSerializer,
)

from core.utils.response import error_response, success_response


class UserProfileService:
    def get_profiles(self):
        try:
            profile_dicts = fetch_user_profiles()

            for profile in profile_dicts:
                user_dicts = fetch_user(profile)
                serializer = UserOutputSerializer(user_dicts)
                profile["user"] = serializer.data

            serializer = UserProfileSerializer(profile_dicts, many=True)
            profiles = serializer.data

            return success_response(
                data=profiles,
                message="User profiles found successfully",
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="User profile list retrieval failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_profile(self, user_id):
        try:
            with connection.cursor() as c:
                c.execute(
                    "SELECT * FROM users_user_profile WHERE user_id=%s", [user_id]
                )
                result = c.fetchone()

                columns = [col[0] for col in c.description]
                profile_dicts = dict(zip(columns, result))

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
                serializer = UserSerializer(user_dicts)
                profile_dicts["user"] = serializer.data

            serializer = UserProfileOutputSerializer(profile_dicts)
            profile = serializer.data

            return success_response(
                profile,
                message="User profiles found successfully",
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="User profile list retrieval failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, payload, user_id):
        try:
            payload = payload or {}
            id = payload.get("id", uuid.uuid4())
            first_name = payload.get("first_name", "")
            last_name = payload.get("last_name", "")
            dob = payload.get("dob", None)
            gender = payload.get("gender", None)
            address = payload.get("address", "")
            phone = payload.get("phone", "")
            created_at = payload.get("created_at", timezone.now())
            updated_at = timezone.now()

            with connection.cursor() as c:
                c.execute(
                    """INSERT INTO users_user_profile (id, first_name, last_name, dob, gender, address, phone, created_at, updated_at, user_id)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
                    """,
                    [
                        id,
                        first_name,
                        last_name,
                        dob,
                        gender,
                        address,
                        phone,
                        created_at,
                        updated_at,
                        user_id,
                    ],
                )
                result = c.fetchone()
                if not result:
                    raise Exception("User profile creation failed")

                columns = []
                for col in c.description:
                    columns.append(col[0])

            profile_dicts = dict(zip(columns, result))

            user_dicts = fetch_user(profile_dicts)
            serializer = UserOutputSerializer(user_dicts)
            profile_dicts["user"] = serializer.data

            serializer = UserProfileSerializer(profile_dicts)
            profile = serializer.data

            return success_response(
                profile,
                message="User profile created succesfully",
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="User profile creation failed",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, payload, user_id):
        try:
            with connection.cursor() as c:
                c.execute(
                    "SELECT * FROM users_user_profile WHERE user_id=%s",
                    [user_id],
                )
                result = c.fetchone()
                if not result:
                    raise Exception("Profile not found for this user")

                columns = []
                for col in c.description:
                    columns.append(col[0])

                old_profile = dict(zip(columns, result))  # TODO selectors till here
                first_name = payload.get("first_name", old_profile.get("first_name"))
                last_name = payload.get("last_name", old_profile.get("last_name"))
                dob = payload.get("dob", old_profile.get("dob"))
                gender = payload.get("gender", old_profile.get("gender"))
                address = payload.get("address", old_profile.get("address"))
                phone = payload.get("phone", old_profile.get("phone"))
                updated_at = timezone.now()

                c.execute(
                    """UPDATE users_user_profile SET
                    first_name=%s, last_name=%s, dob=%s, gender=%s, address=%s, phone=%s, updated_at=%s 
                    WHERE user_id=%s RETURNING *;
                    """,
                    [
                        first_name,
                        last_name,
                        dob,
                        gender,
                        address,
                        phone,
                        updated_at,
                        user_id,
                    ],
                )
                result = c.fetchone()
                if not result:
                    raise Exception("User profile updation failed")

                columns = []
                for col in c.description:
                    columns.append(col[0])

            profile_dicts = dict(zip(columns, result))
            # TODO verify if this works

            user_dicts = fetch_user(profile_dicts)
            serializer = UserOutputSerializer(user_dicts)
            profile_dicts["user"] = serializer.data

            serializer = UserProfileSerializer(profile_dicts)
            profile = serializer.data

            return success_response(
                profile,
                message="User profile updated succesfully",
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
                    "DELETE FROM users_user_profile WHERE user_id=%s RETURNING TRUE;",
                    [id],
                )
                result = c.fetchone()

                if not result:
                    return error_response(
                        error="Invalid user ID",
                        message="Profile does not exist",
                        status=status.HTTP_404_NOT_FOUND,
                    )

            return success_response(
                message="User profile deleted successfully",
                status=status.HTTP_204_NO_CONTENT,
            )

        except DatabaseError as e:
            return error_response(
                error=str(e),
                message="Database error",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def soft_delete(self, id):
        try:
            manager = UserProfile.objects.get(id=id)
            user = manager.user
            user.is_active = False

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

    def hard_delete(self, id):
        try:
            manager = UserProfile.objects.get(id=id)
            user = manager.user

            manager.delete()
            user.delete()

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
