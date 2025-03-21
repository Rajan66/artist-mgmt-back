from django.urls import path

from authentication.views import TokenRefreshView, UserLoginView, UserRegisterView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh-token"),
]
