from rest_framework import status

from authentication.helpers import JWTAuthentication
from authentication.serializers import UserLoginSerializer
from core.utils.response import error_response, success_response


class AuthService:
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                serializer.errors, "Validation failed", status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data["user"]
        jwt_auth = JWTAuthentication()
        token = jwt_auth.get_tokens(user)
        data = {
            "id": user.id,
            "email": user.email,
            "access_token": token[0],
            "refresh_token": token[1],
        }

        return success_response(data, "login successful", status.HTTP_200_OK)
