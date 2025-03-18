from django.urls import path

from albums.views.album import AlbumDetailView, AlbumListView
from albums.views.song import SongCreateView, SongDetailView, SongListView

urlpatterns = [
    # Songs
    path("songs/", SongListView.as_view(), name="song-list"),
    path("<str:album_id>/songs/", SongCreateView.as_view(), name="song-create"),
    path("<str:album_id>/songs/<str:pk>", SongDetailView.as_view(), name="song-delete"),
    # Albums
    path("<str:album_id>/", AlbumDetailView.as_view(), name="album-detail"),
    path("", AlbumListView.as_view(), name="album-list"),
]
