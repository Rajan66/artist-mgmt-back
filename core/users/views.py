from authentication.helpers import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from users.services import UserService


class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_service = UserService()
        response = user_service.list()
        return response
