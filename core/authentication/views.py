from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from authentication.services import AuthService


class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        auth_service = AuthService()
        response = auth_service.login(request)
        return response


class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        auth_service = AuthService()
        response = auth_service.register(request)
        return response
