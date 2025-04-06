from django.urls import path

from authentication.views import (
    TokenBlacklistView,
    TokenRefreshView,
    UserCreateView,
    UserLoginView,
    UserRegisterView,
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("register/profile/", UserCreateView.as_view(), name="user-create"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="blacklist-token"),
]
