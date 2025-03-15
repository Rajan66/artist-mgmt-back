from authentication.helpers import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.services.user import UserService


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
    user_service = UserService()

    def get(self, request, pk):
        response = self.user_service.get_user(id=pk)
        return response

    def put(self, request, pk):
        response = self.user_service.update(id=pk, payload=request.data)
        return response

    def delete(self, request, pk):
        response = self.user_service.delete(id=pk)
        return response
