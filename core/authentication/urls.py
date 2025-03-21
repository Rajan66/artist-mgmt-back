from django.urls import path

from authentication.views import (
    TokenBlacklistView,
    TokenRefreshView,
    UserLoginView,
    UserRegisterView,
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="blacklist-token"),
]
