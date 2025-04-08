from django.urls import path

from artists.views import (
    ArtistDetailView,
    ArtistHardDeleteView,
    ArtistListView,
    ArtistSoftDeleteView,
    ArtistUnbanView,
    ArtistUserView,
    ManagerArtistView,
)

urlpatterns = [
    path(
        "<str:pk>/delete/hard/",
        ArtistHardDeleteView.as_view(),
        name="artist-hard-delete",
    ),
    path(
        "<str:pk>/delete/soft/",
        ArtistSoftDeleteView.as_view(),
        name="artist-soft-delete",
    ),
    path(
        "<str:pk>/unban/",
        ArtistUnbanView.as_view(),
        name="artist-unban",
    ),
    path("<str:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
    path("users/<str:user_id>/", ArtistUserView.as_view(), name="artist-user"),
    path(
        "managers/<str:manager_id>/",
        ManagerArtistView.as_view(),
        name="manager-artists",
    ),
    path("", ArtistListView.as_view(), name="artist-list"),
]
