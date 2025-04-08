from rest_framework.views import APIView

from stats.services import StatService

stat_service = StatService()


class ManagerStatsView(APIView):
    def get(self, request, pk):
        response = stat_service.get_manager_stats(id=pk)
        return response


class AdminStatsView(APIView):
    def get(self, request):
        response = stat_service.get_all_stats()
        return response


class ManagerGenreStatsView(APIView):
    def get(self, request, pk):
        response = stat_service.get_manager_genre(manager_id=pk)
        return response


class AdminGenreStatsView(APIView):
    def get(self, request):
        response = stat_service.get_all_genre()
        return response


class ManagerSongsArtistView(APIView):
    def get(self, request, pk):
        response = stat_service.get_manager_artist_songs(manager_id=pk)
        return response


class AdminSongsArtistView(APIView):
    def get(self, request):
        response = stat_service.get_all_artist_songs()
        return response


class ManagerAlbumsArtistView(APIView):
    def get(self, request, pk):
        response = stat_service.get_manager_artist_albums(manager_id=pk)
        return response


class AdminAlbumsArtistView(APIView):
    def get(self, request):
        response = stat_service.get_all_artist_albums()
        return response


class ManagerRecentSongsView(APIView):
    def get(self, request, pk):
        response = stat_service.get_manager_recent_songs(manager_id=pk)
        return response


class AdminRecentSongsView(APIView):
    def get(self, request):
        response = stat_service.get_all_recent_songs()
        return response
