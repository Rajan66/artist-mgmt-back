from rest_framework.views import APIView

from artists.services import ArtistService

aritst_service = ArtistService()


class ArtistListView(APIView):
    def get(self, request):
        response = aritst_service.get_artists()
        return response
