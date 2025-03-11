from rest_framework.views import exception_handler

from authentication.exceptions import CustomAuthenticationException
from core.utils.response import error_response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, CustomAuthenticationException):
        return error_response(
            {
                "error": str(exc),
                "message": "Authenication failed. Please check your credentials.",
            }
        )

    return response
