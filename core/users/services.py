from rest_framework import status

from core.utils.response import success_response
from users.exceptions import CustomUserException
from users.models import CustomUser as User
from users.serializers import UserSerializer


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
