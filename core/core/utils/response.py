from rest_framework import status
from rest_framework.response import Response


def success_response(
    data=None,
    message="Success",
    status=status.HTTP_200_OK,
    request=None,  # 👈 new
):
    data = data or []

    if request is not None:
        try:
            page = int(request.GET.get("page", 1))
            page_size = int(request.GET.get("page_size", 10))

            total = len(data)
            start = (page - 1) * page_size
            end = start + page_size
            paginated_data = data[start:end]

            return Response(
                {
                    "data": paginated_data,
                    "message": message,
                    "pagination": {
                        "page": page,
                        "page_size": page_size,
                        "count": total,
                    },
                },
                status=status,
            )

        except Exception:
            pass

    return Response(
        {
            "data": data,
            "message": message,
        },
        status=status,
    )


def error_response(
    error=None,
    message="Error",
    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
):
    return Response(
        {
            "error": error,
            "message": message,
        },
        status=status,
    )
