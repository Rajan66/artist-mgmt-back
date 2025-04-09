from django.urls import path

from authentication.views import (
    ChangePasswordView,
    CheckAndSendMail,
    ForgotPasswordView,
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
    path("password/change/", ChangePasswordView.as_view(), name="change-password"),
    path("password/forgot/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("password/forgot/mail/", CheckAndSendMail.as_view(), name="forgot-send-mail"),
]
