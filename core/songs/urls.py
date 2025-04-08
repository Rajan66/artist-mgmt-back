from django.urls import path

from songs.csv.views import AdminCSVView, ArtistCSVView, ManagerCSVView
from songs.views import (
    AlbumSongView,
    ArtistSongView,
    ManagerSongView,
    SongDetailView,
    SongListView,
)

urlpatterns = [
    # Songs
    path("<str:pk>/", SongDetailView.as_view(), name="song-detail"),
    path("artists/<str:pk>/", ArtistSongView.as_view(), name="artist-song"),
    path("albums/<str:pk>/", AlbumSongView.as_view(), name="album-song"),
    path("managers/<str:manager_id>/", ManagerSongView.as_view(), name="manager-songs"),
    path("", SongListView.as_view(), name="song-list"),
    # Export CSV
    path("csv/export/admin/", AdminCSVView.as_view(), name="admin-export-csv"),
    path(
        "csv/export/manager/<str:pk>/",
        ManagerCSVView.as_view(),
        name="manager-export-csv",
    ),
    path(
        "csv/export/artist/<str:pk>/", ArtistCSVView.as_view(), name="artist-export-csv"
    ),
    # Import CSV
    path("csv/import/admin/", AdminCSVView.as_view(), name="admin-import-csv"),
    path(
        "csv/import/manager/<str:pk>/",
        ManagerCSVView.as_view(),
        name="manager-import-csv",
    ),
    path(
        "csv/import/artist/<str:pk>/", ArtistCSVView.as_view(), name="artist-import-csv"
    ),
]
