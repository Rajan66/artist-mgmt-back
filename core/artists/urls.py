from django.urls import path

from artists.views import (
    ArtistDetailView,
    ArtistListView,
    ArtistUserView,
    ManagerArtistView,
)

urlpatterns = [
    path("<str:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
    path("users/<str:user_id>/", ArtistUserView.as_view(), name="artist-user"),
    path(
        "managers/<str:manager_id>/",
        ManagerArtistView.as_view(),
        name="manager-artists",
    ),
    path("", ArtistListView.as_view(), name="artist-list"),
]
