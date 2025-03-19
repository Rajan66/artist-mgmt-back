from rest_framework.views import APIView

from songs.services import SongService

song_service = SongService()


class SongListView(APIView):
    def get(self, request):
        response = song_service.get_songs()
        return response

    def post(self, request):
        pass


class SongDetailView(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
