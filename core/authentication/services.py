from rest_framework import status
from rest_framework.response import Response

from authentication.helpers import JWTAuthentication as jwt
from authentication.serializers import UserLoginSerializer


def send_response(data, message: str, status: status):
    return Response({"data": data, "message": message}, status=status)


class AuthService:
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            # throw exception here from django here
            return send_response(
                None, "something went wrong", status.HTTP_400_BAD_REQUEST
            )

        user = serializer.create(serializer.validated_data)
        token = jwt.get_tokens(None, user)
        data = {
            "id": user.id,
            "email": user.email,
            "access_token": token[0],
            "refresh_token": token[1],
        }

        return send_response(data, "login successful", status.HTTP_200_OK)
