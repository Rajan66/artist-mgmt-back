import datetime
from urllib.parse import unquote

from django.core.mail import send_mail
from django.core.signing import Signer
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from users.models import CustomUser as User

from authentication.exceptions import CustomAuthenticationException
from authentication.helpers import JWTAuthentication
from authentication.serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
)
from core.utils.response import error_response, success_response

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
        if not user.is_active:
            raise CustomAuthenticationException(
                detail="User has been blocked or removed.",
                error_type="Authentication error",
                code=status.HTTP_403_FORBIDDEN,
            )

        tokens = jwt_auth.get_tokens(user)
        data = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
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
            "role": user.role,
            "access_token": tokens[0],
            "refresh_token": tokens[1],
        }

        return success_response(data, "Token refresh successful", status.HTTP_200_OK)

    def blacklist_token(self, request):
        try:
            authorization = request.headers.get("Authorization")
            if authorization:
                token = authorization.split(" ")[1]
                jwt_auth.blacklist_token(token)
                return success_response(
                    None, "Token blacklisted successful", status.HTTP_204_NO_CONTENT
                )
            else:
                raise Exception("Invalid token type")
        except Exception as e:
            raise CustomAuthenticationException(
                detail=str(e),
                code=status.HTTP_403_FORBIDDEN,
                error_type="Authentication error",
            )

    def change_pw(self, payload):
        serializer = ChangePasswordSerializer(data=payload)

        if not serializer.is_valid():
            raise CustomAuthenticationException(
                detail=serializer.errors,
                error_type="Validation error",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response("Password changed successfully", status.HTTP_200_OK)

    def forgot_pw_check_user(self, payload):
        try:
            email = payload.get("email")
            user = User.objects.filter(email=email).first()
            if not user:
                raise ValidationError("Invalid email")

            claims = {
                "email": email,
                "iat": timezone.now().isoformat(),
                "exp": (timezone.now() + timezone.timedelta(minutes=15)).isoformat(),
            }
            signer = Signer()
            url_key = signer.sign_object(claims)

            send_mail(
                "Password Reset Request",
                f"Hello,\n\nWe received a request to reset your password. Please click the link below to reset it:\n\n"
                f"http://localhost:3000/forgot/password/{url_key}/\n\n"
                "If you didn't request a password reset, please ignore this email. Your password will remain unchanged.\n\n"
                "Best regards,\nVoxCloud",
                "rajanmaharjan042@gmail.com",
                [email],
                fail_silently=False,
            )
            return success_response("Link sent successfully", status.HTTP_200_OK)

        except ValidationError as e:
            return error_response(
                error=e.message if hasattr(e, "message") else str(e),
                message="Validation error",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to send mail",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def forgot_pw(self, payload):
        try:
            raw_token = payload.get("token")
            token = unquote(raw_token)

            signer = Signer()
            claims = signer.unsign_object(token)
            exp = claims.get("exp")
            email = claims.get("email")

            if exp:
                expiration_time = datetime.datetime.fromisoformat(exp)
                current_time = timezone.now()

                if current_time > expiration_time:
                    return error_response(
                        error="Token has expired",
                        message="The reset token has expired. Please request a new one.",
                        status=status.HTTP_410_GONE,
                    )

            user = User.objects.filter(email=email).first()
            if not user:
                raise ValidationError("Invalid email.")

            serializer = ForgotPasswordSerializer(data=payload)

            if not serializer.is_valid():
                raise CustomAuthenticationException(
                    detail=serializer.errors,
                    error_type="Validation error",
                    code=status.HTTP_400_BAD_REQUEST,
                )
            validated_data = serializer.validated_data
            user.set_password(validated_data["password"])
            user.save()

            return success_response("Password changed successfully", status.HTTP_200_OK)

        except ValidationError as e:
            return error_response(
                error=e.message if hasattr(e, "message") else str(e),
                message="Validation error",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to send mail",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
