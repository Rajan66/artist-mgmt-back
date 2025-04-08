from django.urls import path

from .views import (
    AdminAlbumsArtistView,
    AdminGenreStatsView,
    AdminRecentSongsView,
    AdminSongsArtistView,
    AdminStatsView,
    ManagerAlbumsArtistView,
    ManagerGenreStatsView,
    ManagerRecentSongsView,
    ManagerSongsArtistView,
    ManagerStatsView,
)

urlpatterns = [
    path("managers/<str:pk>/", ManagerStatsView.as_view(), name="manager-stats"),
    path("admin/", AdminStatsView.as_view(), name="admin-stats"),
    path(
        "managers/<str:pk>/genre/",
        ManagerGenreStatsView.as_view(),
        name="manager-genre-stats",
    ),
    path(
        "admin/genre/",
        AdminGenreStatsView.as_view(),
        name="admin-genre-stats",
    ),
    path(
        "managers/<str:pk>/songs/",
        ManagerSongsArtistView.as_view(),
        name="manager-artist-songs-stats",
    ),
    path(
        "admin/songs/",
        AdminSongsArtistView.as_view(),
        name="admin-artist-songs-stats",
    ),
    path(
        "managers/<str:pk>/albums/",
        ManagerAlbumsArtistView.as_view(),
        name="manager-artist-songs-stats",
    ),
    path(
        "admin/albums/",
        AdminAlbumsArtistView.as_view(),
        name="admin-artist-songs-stats",
    ),
    path(
        "managers/<str:pk>/songs/recent/",
        ManagerRecentSongsView.as_view(),
        name="manager-recent-songs-stats",
    ),
    path(
        "admin/songs/recent/",
        AdminRecentSongsView.as_view(),
        name="admin-recent-songs-stats",
    ),
]
