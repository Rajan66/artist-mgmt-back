from albums.services.album import AlbumService
from rest_framework.views import APIView

album_service = AlbumService()


class AlbumListView(APIView):
    def get(self, request):
        print("Hello")
        response = album_service.get_albums()
        return response

    def post(self, request, album_id):
        pass


class AlbumDetailView(APIView):
    def get(self, request, album_id, pk):
        pass

    def update(self, request, album_id, pk):
        pass

    def delete(self, request, album_id, pk):
        pass
