import uuid

from django.db import connection
from django.utils import timezone
from rest_framework import status
from users.models import CustomUser as User
from users.serializers import UserSerializer

from core.utils.response import error_response, success_response


class UserService:
    def list(self):
        users = User.objects.all()
        if not users.exists:
            return success_response(
                [],
                message="No user found",
                status=status.HTTP_200_OK,
            )
        serializer = UserSerializer(users, many=True)
        user_list = serializer.data

        return success_response(
            user_list,
            message="Users found sucessfully",
            status=status.HTTP_200_OK,
        )

    def get_users(self):
        with connection.cursor() as c:
            c.execute("SELECT * FROM users_customuser")

            columns = []
            for col in c.description:
                columns.append(col[0])

            results = c.fetchall()

        # Convert each row to a dict
        user_dicts = [dict(zip(columns, row)) for row in results]

        serializer = UserSerializer(user_dicts, many=True)
        users = serializer.data

        return success_response(
            users,
            message="Users found successfully",
            status=status.HTTP_200_OK,
        )

    def get_user(self, id):
        with connection.cursor() as c:
            c.execute("SELECT * FROM users_customuser where id=%s", [id])

            columns = []
            for col in c.description:
                columns.append(col[0])

            result = c.fetchone()

        user_dicts = dict(zip(columns, result))
        serializer = UserSerializer(user_dicts)
        user = serializer.data

        return success_response(
            user,
            message="Users found successfully",
            status=status.HTTP_200_OK,
        )

    def create(self, payload: User):
        id = uuid.uuid4()
        email = payload.get("email")
        password = payload.get("password")
        role = payload.get("role")
        is_active = payload.get("is_active") if payload.get("is_active") else False
        is_staff = payload.get("is_staff") if payload.get("is_staff") else False
        is_superuser = (
            payload.get("is_superuser") if payload.get("is_superuser") else False
        )

        date_joined = timezone.now()
        updated_at = timezone.now()

        with connection.cursor() as c:
            c.execute(
                """INSERT INTO users_customuser ("id", "email", "password", "role", "is_active", "is_staff", "is_superuser", "date_joined", "updated_at") values ( 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
                """,
                [
                    id,
                    email,
                    password,
                    role,
                    is_active,
                    is_staff,
                    is_superuser,
                    date_joined,
                    updated_at,
                ],
            )

            result = c.fetchone()
            columns = []
            for col in c.description:
                columns.append(col[0])

        user_dicts = dict(zip(columns, result))
        serializer = UserSerializer(user_dicts)
        user = serializer.data

        return success_response(
            user,
            message="User created sucessfully",
            status=status.HTTP_201_CREATED,
        )

    def update(self, payload, id):
        with connection.cursor() as c:
            c.execute("SELECT * FROM users_customuser WHERE id=%s", [id])

            fetch_result = c.fetchone()

            if not fetch_result:
                return error_response(
                    error="Invalid user id",
                    message="User does not exist",
                    status=status.HTTP_404_NOT_FOUND,
                )

            columns = []
            for col in c.description:
                columns.append(col[0])

            old_user = dict(zip(columns, fetch_result))

            email = (
                payload.get("email") if payload.get("email") else old_user.get("email")
            )
            role = payload.get("role") if payload.get("role") else old_user.get("role")
            is_active = (
                payload.get("is_active")
                if payload.get("is_active")
                else old_user.get("is_active")
            )
            is_staff = (
                payload.get("is_staff")
                if payload.get("is_staff")
                else old_user.get("is_staff")
            )
            is_superuser = (
                payload.get("is_superuser")
                if payload.get("is_superuser")
                else old_user.get("is_superuser")
            )

            updated_at = timezone.now()

            c.execute(
                """UPDATE users_customuser SET email=%s, role=%s, is_active=%s, is_staff=%s, is_superuser=%s, updated_at=%s 
                    WHERE id=%s RETURNING *;
                """,
                [
                    email,
                    role,
                    is_active,
                    is_staff,
                    is_superuser,
                    updated_at,
                    id,
                ],
            )

            updated_result = c.fetchone()
            columns = []
            for col in c.description:
                columns.append(col[0])

        user_dicts = dict(zip(columns, updated_result))
        serializer = UserSerializer(user_dicts)
        updated_user = serializer.data

        return success_response(
            updated_user,
            message="User updated sucessfully",
            status=status.HTTP_201_CREATED,
        )

    def delete(self, id):
        with connection.cursor() as c:
            c.execute(
                "DELETE FROM users_customuser WHERE id = %s RETURNING TRUE;", [id]
            )

            result = c.fetchone()
            if not result:
                return error_response(
                    error="Invalid user id",
                    message="User does not exist",
                    status=status.HTTP_404_NOT_FOUND,
                )

        return success_response(
            message="User deleted successfully", status=status.HTTP_204_NO_CONTENT
        )
