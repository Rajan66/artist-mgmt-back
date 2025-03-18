from rest_framework.views import APIView


class SongListView(APIView):
    def get(self, request):
        pass


class SongCreateView(APIView):
    def post(self, request, album_id):
        pass


class SongDetailView(APIView):
    def get(self, request, album_id, pk):
        pass

    def update(self, request, album_id, pk):
        pass

    def delete(self, request, album_id, pk):
        pass
