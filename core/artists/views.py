from rest_framework.views import APIView

from artists.services import ArtistService

aritst_service = ArtistService()


class ArtistListView(APIView):
    def get(self, request):
        response = aritst_service.get_artists()
        return response


class ArtistDetailView(APIView):
    def get(self, request, pk):
        response = aritst_service.get_artist(id=pk)
        return response

    def post(self, request, pk):
        response = aritst_service.create(payload=request.data, id=pk)
        return response

    def put(self, request, pk):
        response = aritst_service.update(payload=request.data, id=pk)
        return response

    def delete(self, request, pk):
        response = aritst_service.delete(id=pk)
        return response


class ArtistUserView(APIView):
    def get(self, request, user_id):
        response = aritst_service.get_artist_with_user(id=user_id)
        return response


class ManagerArtistView(APIView):
    def get(self, request, manager_id):
        response = aritst_service.get_manager_artists(manager_id=manager_id)
        return response
