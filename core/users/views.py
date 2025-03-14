from authentication.helpers import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.services import UserService


class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    user_service = UserService()

    def get(self, request):
        response = self.user_service.get_users()
        return response

    def post(self, request):
        user = request.data
        response = self.user_service.create(user)
        return response


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user_service = UserService()
        response = user_service.get_user_v2(id=pk)
        return response
