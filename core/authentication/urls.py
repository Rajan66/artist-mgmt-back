from django.urls import path

from authentication.views import UserLoginView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    # path("register/", UserLoginView.as_view(), name="login"),
]
