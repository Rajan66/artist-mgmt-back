from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Something went horribly wrong in the server.")
    default_code = "internal_server_error"
    error = "server error"

    def __init__(self, detail, code, error):
        if detail:
            self.detail = detail
        if code:
            self.code = code
        if error:
            self.error = error
