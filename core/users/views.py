from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return HttpResponse("Hello world")
