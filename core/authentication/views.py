from rest_framework.views import APIView

from authentication.services import AuthService


class UserLoginView(APIView):
    def post(self, request):
        auth_service = AuthService()
        response = auth_service.login(request)
        return response
