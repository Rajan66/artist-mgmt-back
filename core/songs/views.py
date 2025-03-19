from rest_framework.views import APIView

from songs.services import SongService

song_service = SongService()


class SongListView(APIView):
    def get(self, request):
        response = song_service.get_songs()
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
        response = song_service.get_artist_songs(artist_id=pk)
        return response


class AlbumSongView(APIView):
    def get(self, request, pk):
        response = song_service.get_album_songs(album_id=pk)
        return response
