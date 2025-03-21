import jwt
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from users.models import CustomUser as User

from authentication.exceptions import CustomAuthenticationException
from authentication.models import TokenBlacklist
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
            id = self.check_claims(token, "access")
            user = (
                User.objects.filter(id=id)
                .only("id", "email", "role", "is_active", "is_staff", "last_login")
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
            "role": user.role,
            "iat": timezone.now(),
            "exp": timezone.now() + timezone.timedelta(minutes=expiry),
            "type": "access",
        }

        access_token = jwt.encode(
            payload=payload, key=settings.SECRET_KEY, algorithm="HS256"
        )
        isBlacklisted = self.check_blacklist(access_token)
        if isBlacklisted:
            raise CustomAuthenticationException(
                detail="Blacklisted token!",
                code=status.HTTP_403_FORBIDDEN,
                error_type="Authenication error",
            )
        return access_token

    def generate_refresh_token(self, user: User, *args, **kwargs):
        expiry = int(settings.env("REFRESH_EXPIRY_TIME"))

        payload = {
            "id": str(user.id),
            "email": user.email,
            "role": user.role,
            "iat": timezone.now(),
            "exp": timezone.now() + timezone.timedelta(days=expiry),
            "type": "refresh",
        }

        refresh_token = jwt.encode(
            payload=payload, key=settings.SECRET_KEY, algorithm="HS256"
        )
        isBlacklisted = self.check_blacklist(refresh_token)
        if isBlacklisted:
            raise CustomAuthenticationException(
                detail="Blacklisted token!",
                code=status.HTTP_403_FORBIDDEN,
                error_type="Authenication error",
            )
        return refresh_token

    def get_tokens(self, user, *args, **kwargs):
        access_token = self.generate_access_token(user)
        refresh_token = self.generate_refresh_token(user)

        return [access_token, refresh_token]

    def check_claims(self, token, token_type):
        isBlacklisted = self.check_blacklist(token)
        if isBlacklisted:
            raise CustomAuthenticationException(
                detail="Blacklisted token!",
                code=status.HTTP_403_FORBIDDEN,
                error_type="Authenication error",
            )
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

        if payload["type"] != token_type:
            raise CustomAuthenticationException(
                detail="Invalid token type!",
                code=status.HTTP_403_FORBIDDEN,
                error_type="Authenication error",
            )
        return payload["id"]

    def validate_refresh(self, request):
        try:
            authorization = request.headers.get("Authorization")
            if authorization:
                token = authorization.split(" ")[1]
            else:
                raise Exception("Invalid token type")
            user_id = self.check_claims(token, "refresh")
            self.blacklist_token(token)

            return user_id
        except Exception as e:
            raise CustomAuthenticationException(
                detail=str(e),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_type="Authenication error",
            )

    def check_blacklist(self, token):
        try:
            token_found = TokenBlacklist.objects.filter(token=token).first()
            return True if token_found else False

        except Exception as e:
            raise CustomAuthenticationException(
                detail=str(e),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_type="Authenication error",
            )

    def blacklist_token(self, token):
        token = TokenBlacklist.objects.create(token=token)
