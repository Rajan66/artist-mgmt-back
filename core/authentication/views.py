from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from authentication.services import AuthService

auth_service = AuthService()


class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        response = auth_service.login(request)
        return response


class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        response = auth_service.register(request)
        return response


class TokenRefreshView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        response = auth_service.refresh_token(request)
        return response


class TokenBlacklistView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        response = auth_service.blacklist_token(request)
        return response
