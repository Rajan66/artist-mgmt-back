from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from users.services.user import UserService

from authentication.services import AuthService

auth_service = AuthService()
user_service = UserService()


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


class UserCreateView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        response = user_service.create(payload=request.data)
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


class ChangePasswordView(APIView):
    def post(self, request):
        response = auth_service.change_pw(payload=request.data)
        return response


class CheckAndSendMail(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        response = auth_service.forgot_pw_check_user(payload=request.data)
        return response


class ForgotPasswordView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        response = auth_service.forgot_pw(payload=request.data)
        return response
