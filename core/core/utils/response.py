from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, message="Success", status=status.HTTP_200_OK):
    return Response({"data": data, "message": message}, status=status)


def error_response(
    error=None, message="Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR
):
    print(error, message, status)
    return Response({"error": error, "message": message}, status=status)
