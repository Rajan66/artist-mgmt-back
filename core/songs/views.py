from albums.services.album import AlbumService
from rest_framework.views import APIView

album_service = AlbumService()


class SongListView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class SongDetailView(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
