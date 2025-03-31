from django.db import DatabaseError, IntegrityError, connection
from django.utils import timezone
from rest_framework import status
from users.models.user import CustomUser as User
from users.serializers import UserSerializer
from users.utils import create_profile

from core.utils.response import error_response, success_response
from core.utils.utils import convert_formdata_to_json


class UserService:
    def get_users(self):
        try:
            with connection.cursor() as c:
                c.execute("SELECT * FROM users_customuser")
                columns = [col[0] for col in c.description]
                results = c.fetchall()

            user_dicts = [dict(zip(columns, row)) for row in results]
            serializer = UserSerializer(user_dicts, many=True)

            return success_response(
                serializer.data,
                message="Users found successfully",
                status=status.HTTP_200_OK,
            )
        except DatabaseError as e:
            return error_response(
                error=str(e),
                message="Database error",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_user(self, id):
        try:
            with connection.cursor() as c:
                c.execute("SELECT * FROM users_customuser WHERE id=%s", [id])
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

            return success_response(
                serializer.data,
                message="User found successfully",
                status=status.HTTP_200_OK,
            )
        except DatabaseError as e:
            return error_response(
                error="Database error",
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, payload):
        try:
            email = payload.get("email")
            password = payload.get("password")
            role = payload.get("role").lower()

            json = convert_formdata_to_json(payload)
            artists_json = json.get("artist")

            if role not in ["artist", "artist_manager", "super_admin"]:
                raise Exception("Invalid role. Please check the role again.")

            user_obj = User.objects.create(email=email, role=role)
            user_obj.set_password(password)
            user_obj.save()

            serializer = UserSerializer(user_obj)
            user = serializer.data

            if user.get("role") == "artist":
                if not artists_json:
                    success = create_profile(profile=None, user=user)
                else:
                    success = create_profile(profile=artists_json, user=user)
            elif user.get("role") in ["artist_manager", "super_admin"]:
                if not artists_json:
                    success = create_profile(profile=None, user=user)
                else:
                    success = create_profile(profile=artists_json, user=user)
            else:
                raise Exception("Invalid role. Please check the role again.")

            if not success:
                self.delete(id=user.get("id"))
                raise Exception("Invalid manager.")

            return success_response(
                user,
                message="User created successfully",
                status=status.HTTP_201_CREATED,
            )

        except IntegrityError:
            return error_response(
                error="A user with this email may already exist.",
                message="Integrity error",
                status=status.HTTP_400_BAD_REQUEST,
            )

        except DatabaseError as e:
            return error_response(
                error=str(e),
                message="Database error",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return error_response(
                error=str(e),
                message="User creation failed",
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, payload, id):
        try:
            with connection.cursor() as c:
                c.execute("SELECT * FROM users_customuser WHERE id=%s", [id])
                fetch_result = c.fetchone()

                if not fetch_result:
                    return error_response(
                        error="Invalid user ID",
                        message="User does not exist",
                        status=status.HTTP_404_NOT_FOUND,
                    )

                columns = [col[0] for col in c.description]
                old_user = dict(zip(columns, fetch_result))

                email = payload.get("email", old_user.get("email"))
                role = payload.get("role", old_user.get("role"))
                is_active = payload.get("is_active", old_user.get("is_active"))
                is_staff = payload.get("is_staff", old_user.get("is_staff"))
                is_superuser = payload.get("is_superuser", old_user.get("is_superuser"))
                updated_at = timezone.now()

                c.execute(
                    """UPDATE users_customuser SET email=%s, role=%s, is_active=%s, is_staff=%s, is_superuser=%s, updated_at=%s 
                        WHERE id=%s RETURNING *;
                    """,
                    [email, role, is_active, is_staff, is_superuser, updated_at, id],
                )

                updated_result = c.fetchone()
                columns = [col[0] for col in c.description]

            user_dicts = dict(zip(columns, updated_result))
            serializer = UserSerializer(user_dicts)

            return success_response(
                serializer.data,
                message="User updated successfully",
                status=status.HTTP_200_OK,
            )

        except IntegrityError:
            return error_response(
                error="Failed to update user due to data constraints.",
                message="Integrity error",
                status=status.HTTP_400_BAD_REQUEST,
            )

        except DatabaseError as e:
            return error_response(
                error=str(e),
                message="Database error",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, id):
        try:
            with connection.cursor() as c:
                c.execute(
                    "DELETE FROM users_customuser WHERE id = %s RETURNING TRUE;", [id]
                )
                result = c.fetchone()

                if not result:
                    return error_response(
                        error="Invalid user ID",
                        message="User does not exist",
                        status=status.HTTP_404_NOT_FOUND,
                    )

            return success_response(
                message="User deleted successfully", status=status.HTTP_204_NO_CONTENT
            )

        except DatabaseError as e:
            return error_response(
                error=str(e),
                message="Database error",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
