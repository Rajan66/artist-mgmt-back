import jwt
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from users.models import CustomUser as User

from authentication.exceptions import CustomAuthenticationException
from core import settings


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization = request.headers.get("Authorization")
        if authorization:
            token = authorization.split(" ")[1]
        else:
            raise CustomAuthenticationException(
                detail="Invalid token!",
                code=status.HTTP_401_UNAUTHORIZED,
                error_type="Authenication error",
            )

        try:
            id = self.check_claims(token)
            user = (
                User.objects.filter(id=id)
                .only("id", "email", "is_active", "is_staff", "last_login")
                .first()
            )

            if not user:
                raise CustomAuthenticationException(
                    "User not found!",
                    code=status.HTTP_404_NOT_FOUND,
                    error_type="User error",
                )

        except jwt.InvalidSignatureError:
            raise CustomAuthenticationException(
                detail="Invalid signature!",
                code=status.HTTP_401_UNAUTHORIZED,
                error_type="Authenication error",
            )
        except jwt.ExpiredSignatureError:
            raise CustomAuthenticationException(
                detail="Token expired!",
                code=status.HTTP_401_UNAUTHORIZED,
                error_type="Authenication error",
            )

        return (user, None)

    def generate_access_token(self, user: User, *args, **kwargs):
        expiry = int(settings.env("ACCESS_EXPIRY_TIME"))
        payload = {
            "id": str(user.id),
            "email": user.email,
            "iat": timezone.now(),
            "exp": timezone.now() + timezone.timedelta(minutes=expiry),
            "type": "access",
        }

        access_token = jwt.encode(
            payload=payload, key=settings.SECRET_KEY, algorithm="HS256"
        )
        return access_token

    def generate_refresh_token(self, user: User, *args, **kwargs):
        expiry = int(settings.env("REFRESH_EXPIRY_TIME"))

        payload = {
            "id": str(user.id),
            "email": user.email,
            "iat": timezone.now(),
            "exp": timezone.now() + timezone.timedelta(days=expiry),
            "type": "refresh",
        }

        refresh_token = jwt.encode(
            payload=payload, key=settings.SECRET_KEY, algorithm="HS256"
        )
        return refresh_token

    def get_tokens(self, user, *args, **kwargs):
        access_token = self.generate_access_token(user)
        refresh_token = self.generate_refresh_token(user)

        return [access_token, refresh_token]

    def check_claims(self, token):
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

        if payload["type"] != "access":
            raise CustomAuthenticationException(detail="Invalid token type!")
        return payload["id"]
