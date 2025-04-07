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


class MonthlyStatsView(APIView):
    def get(self, request, pk):
        response = stat_service.get_manager_monthly_songs(manager_id=pk)
        return response


class AdminMonthlyStatsView(APIView):
    def get(self, request):
        response = stat_service.get_monthly_songs()
        return response
