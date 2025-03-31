from rest_framework.views import exception_handler

from core.utils.exceptions import CustomAPIException
from core.utils.response import error_response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, CustomAPIException):
        return error_response(
            error=exc.error,
            message=str(exc),
            status=exc.status_code,
        )

    return response


def convert_formdata_to_json(payload):
    json_object = {}

    for key, value in payload.items():
        keys = key.replace("]", "").split(
            "["
        )  # Split `artist[dob]` into `["artist", "dob"]`

        current = json_object
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value  # Assign value

    return json_object
