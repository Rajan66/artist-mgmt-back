from django.db import connection
from rest_framework import status
from users.exceptions import CustomUserException
from users.models import CustomUser as User
from users.serializers import UserSerializer

from core.utils.response import success_response


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

    def get_user(self, id):
        user = User.objects.get(id=id)
        if user.DoesNotExist:
            raise CustomUserException(detail="User not found")
        return success_response(
            user,
            message="User found sucessfully",
            status=status.HTTP_200_OK,
        )

    def get_users(self):
        with connection.cursor() as c:
            c.execute("SELECT * FROM users_customuser")

            columns = []
            for col in c.description:
                columns.append(col[0])

            users = c.fetchall()

        # Convert each row to a dict
        user_dicts = [dict(zip(columns, row)) for row in users]

        serializer = UserSerializer(user_dicts, many=True)
        data = serializer.data

        return success_response(
            data,
            message="Users found successfully",
            status=status.HTTP_200_OK,
        )

    def get_user_v2(self, id):
        with connection.cursor() as c:
            c.execute("SELECT * FROM users_customuser where id=%s", [id])

            columns = []
            for col in c.description:
                columns.append(col[0])

            user = c.fetchone()

        user_dicts = dict(zip(columns, user))
        serializer = UserSerializer(user_dicts)
        data = serializer.data

        return success_response(
            data,
            message="Users found successfully",
            status=status.HTTP_200_OK,
        )
