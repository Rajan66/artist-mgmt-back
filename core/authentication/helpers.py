import jwt
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from users.models import CustomUser

from core import settings


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass

    def generate_access_token(self, user: CustomUser, *args, **kwargs):
        expiry = int(settings.env("ACCESS_EXPIRY_TIME"))
        payload = {
            "id": str(user.id),
            "email": user.email,
            "iat": timezone.now(),
            "exp": timezone.now() + timezone.timedelta(minutes=expiry),
        }

        access_token = jwt.encode(
            payload=payload, key=settings.SECRET_KEY, algorithm="HS256"
        )
        return access_token

    def generate_refresh_token(self, user: CustomUser, *args, **kwargs):
        expiry = int(settings.env("REFRESH_EXPIRY_TIME"))

        payload = {
            "id": str(user.id),
            "email": user.email,
            "iat": timezone.now(),
            "exp": timezone.now() + timezone.timedelta(days=expiry),
        }

        refresh_token = jwt.encode(
            payload=payload, key=settings.SECRET_KEY, algorithm="HS256"
        )
        return refresh_token

    def get_tokens(self, user, *args, **kwargs):
        auth = JWTAuthentication()
        access_token = auth.generate_access_token(user)
        refresh_token = auth.generate_refresh_token(user)

        return [access_token, refresh_token]

    def check_expiry(self):
        pass

    def set_claims(self):
        pass

    def extract_claims(self):
        pass
