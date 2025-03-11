from django.utils.translation import gettext_lazy as _
from rest_framework import status

from core.utils.exceptions import CustomAPIException


class CustomAuthenticationException(CustomAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("Authentication credentials were not provided")
    default_error_type = _("Authentication error")
    default_code = "authentication_failed"

    def __init__(self, detail, code, error_type):
        if detail:
            self.detail = detail
        if code:
            self.code = code
        if type:
            self.error_type = error_type
