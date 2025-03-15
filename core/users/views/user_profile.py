from rest_framework.views import APIView
from users.services.user_profile import UserProfileService

user_profile_service = UserProfileService()


class ProfileListView(APIView):
    def get(self, request):
        response = user_profile_service.get_profiles()
        return response


class ProfileDetailView(APIView):
    def get(self, request, user_id):
        response = user_profile_service.get_profile(user_id=user_id)
        return response

    def post(self, request, user_id):
        response = user_profile_service.create(payload=request.data, user_id=user_id)
        return response

    def put(self, request, user_id):
        response = user_profile_service.update(payload=request.data, user_id=user_id)
        return response

    def delete(self, request, user_id):
        response = user_profile_service.delete(id=user_id)
        return response
