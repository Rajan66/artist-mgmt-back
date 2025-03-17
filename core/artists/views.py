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
        response = aritst_service.create(payload=request.data, user_id=pk)
        return response

    def put(self, request, pk):
        response = aritst_service.update(payload=request.data, user_id=pk)
        return response

    def delete(self, request, pk):
        response = aritst_service.delete(id=pk)
        return response
