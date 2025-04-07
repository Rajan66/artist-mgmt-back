from django.urls import path
from users.views.user import UserDetailView, UserListView
from users.views.user_profile import ProfileDetailView, ProfileListView

urlpatterns = [
    path(
        "<str:user_id>/profile/",
        ProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
    path(
        "<str:user_id>/profile/delete/soft/",
        ProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
    path(
        "<str:user_id>/profile/delete/hard",
        ProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
    path("profile/", ProfileListView.as_view(), name="user-profile-list"),
    path("<str:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("", UserListView.as_view(), name="user-list"),
]
