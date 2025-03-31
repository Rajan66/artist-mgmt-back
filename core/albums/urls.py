from django.urls import path

from albums.views.album import (
    AlbumDetailView,
    AlbumListView,
    ArtistAlbumView,
    ManagerAlbumView,
)

urlpatterns = [
    path("<str:album_id>/", AlbumDetailView.as_view(), name="album-detail"),
    path("artists/<str:artist_id>/", ArtistAlbumView.as_view(), name="artist-album"),
    path(
        "managers/<str:manager_id>/", ManagerAlbumView.as_view(), name="manager-albums"
    ),
    path("", AlbumListView.as_view(), name="album-list"),
]
