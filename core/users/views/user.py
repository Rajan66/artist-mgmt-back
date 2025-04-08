from authentication.helpers import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.services.user import UserService

user_service = UserService()


class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = user_service.get_users(request=request)
        return response

    def post(self, request):
        user = request.data
        response = user_service.create(user)
        return response


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        response = user_service.get_user(id=pk)
        return response

    def put(self, request, pk):
        response = user_service.update(id=pk, payload=request.data)
        return response

    def delete(self, request, pk):
        response = user_service.delete(id=pk)
        return response
