from django.urls import path
from users.views.user import UserDetailView, UserListView
from users.views.user_profile import (
    ProfileDetailView,
    ProfileHardDeleteView,
    ProfileListView,
    ProfileSoftDeleteView,
    ProfileUnbanView,
)

urlpatterns = [
    path(
        "<str:user_id>/profile/",
        ProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
    path(
        "<str:pk>/profile/delete/soft/",
        ProfileSoftDeleteView.as_view(),
        name="user-profile-soft-delete",
    ),
    path(
        "<str:pk>/profile/delete/hard/",
        ProfileHardDeleteView.as_view(),
        name="user-profile-hard-delete",
    ),
    path(
        "<str:pk>/profile/unban/",
        ProfileUnbanView.as_view(),
        name="user-profile-unban",
    ),
    path("profile/", ProfileListView.as_view(), name="user-profile-list"),
    path("<str:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("", UserListView.as_view(), name="user-list"),
]
