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

    def delete(self, request, album_id):
        response = album_service.delete(id=album_id)
        return response


class ArtistAlbumView(APIView):
    def get(self, request, artist_id):
        response = album_service.get_artist_albums(id=artist_id)
        return response


class ManagerAlbumView(APIView):
    def get(self, request, manager_id):
        response = album_service.get_manager_albums(manager_id=manager_id)
        return response
