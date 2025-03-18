from albums.services.album import AlbumService
from rest_framework.views import APIView

album_service = AlbumService()


class AlbumListView(APIView):
    def get(self, request):
        response = album_service.get_albums()
        return response

    def post(self, request):
        response = album_service.create(payload=request.data)
        return response


class AlbumDetailView(APIView):
    def get(self, request, album_id):
        response = album_service.get_album(album_id=album_id)
        return response

    def put(self, request, album_id):
        response = album_service.update(payload=request.data, album_id=album_id)
        return response

    def delete(self, request, album_id, pk):
        pass
