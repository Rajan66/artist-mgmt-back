from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from songs.services import SongService

song_service = SongService()


class SongListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        response = song_service.get_songs(request=request)
        return response

    def post(self, request):
        response = song_service.create(payload=request.data)
        return response


class SongDetailView(APIView):
    def get(self, request, pk):
        response = song_service.get_song(id=pk)
        return response

    def put(self, request, pk):
        response = song_service.update(payload=request.data, id=pk)
        return response

    def delete(self, request, pk):
        response = song_service.delete(id=pk)
        return response


class ArtistSongView(APIView):
    def get(self, request, pk):
        response = song_service.get_artist_songs(artist_id=pk, request=request)
        return response


class AlbumSongView(APIView):
    def get(self, request, pk):
        response = song_service.get_album_songs(album_id=pk, request=request)
        return response


class ManagerSongView(APIView):
    def get(self, request, manager_id):
        response = song_service.get_manager_songs(
            manager_id=manager_id, request=request
        )
        return response
