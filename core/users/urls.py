from django.urls import path
from users.views.user import UserDetailView, UserListView

urlpatterns = [
    path("<str:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("", UserListView.as_view(), name="user-list"),
]
