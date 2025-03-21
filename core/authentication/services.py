from rest_framework import status
from users.models import CustomUser as User

from authentication.exceptions import CustomAuthenticationException
from authentication.helpers import JWTAuthentication
from authentication.serializers import UserLoginSerializer, UserRegisterSerializer
from core.utils.response import success_response

jwt_auth = JWTAuthentication()


class AuthService:
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            raise CustomAuthenticationException(
                detail=serializer.errors,
                error_type="Validation error",
                code=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]

        tokens = jwt_auth.get_tokens(user)
        data = {
            "id": user.id,
            "email": user.email,
            "access_token": tokens[0],
            "refresh_token": tokens[1],
        }

        return success_response(data, "login successful", status.HTTP_200_OK)

    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomAuthenticationException(
                detail=serializer.errors,
                error_type="Authentication error",
                code=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        data = serializer.data
        user = User.objects.filter(email=data["email"]).first()
        response_data = {
            "id": user.id,
            "email": user.email,
        }

        return success_response(
            data=response_data,
            message="Registration successful",
            status=status.HTTP_201_CREATED,
        )

    def refresh_token(self, request):
        user_id = jwt_auth.validate_refresh(request)
        user = (
            User.objects.filter(id=user_id)
            .only("id", "email", "role", "is_active", "is_staff", "last_login")
            .first()
        )
        print("User =============>", user)

        tokens = jwt_auth.get_tokens(user)
        data = {
            "id": user.id,
            "email": user.email,
            "access_token": tokens[0],
            "refresh_token": tokens[1],
        }

        return success_response(data, "Token refresh successful", status.HTTP_200_OK)
