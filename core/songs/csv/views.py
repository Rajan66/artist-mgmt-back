from rest_framework.views import APIView
from songs.csv.services import CSVService

csv_service = CSVService()


class AdminCSVView(APIView):
    def get(self, request):
        response = csv_service.admin_export(request)
        return response

    def post(self, request):
        response = csv_service.admin_import(request)
        return response


class ManagerCSVView(APIView):
    def get(self, request, pk):
        response = csv_service.manager_export(request, manager_id=pk)
        return response

    def post(self, request, pk):
        response = csv_service.manager_import(request=request, manager_id=pk)
        return response


class ArtistCSVView(APIView):
    def get(self, request, pk):
        response = csv_service.artist_export(request, user_id=pk)
        return response

    def post(self, request, pk):
        response = csv_service.artist_import(request=request, user_id=pk)
        return response
