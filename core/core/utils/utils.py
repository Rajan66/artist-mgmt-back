from rest_framework.views import exception_handler

from core.utils.exceptions import CustomAPIException
from core.utils.response import error_response


def custom_exception_handler(exc, context):
    print(exc, context)
    response = exception_handler(exc, context)

    if isinstance(exc, CustomAPIException):
        return error_response(
            error=str(exc), message=exc.error_type, status=exc.status_code
        )

    return response
