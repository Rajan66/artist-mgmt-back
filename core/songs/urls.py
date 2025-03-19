from django.urls import path

from songs.views import AlbumSongView, ArtistSongView, SongDetailView, SongListView

urlpatterns = [
    # Songs
    path("", SongListView.as_view(), name="song-list"),
    path("<str:pk>/", SongDetailView.as_view(), name="song-detail"),
    path("artists/<str:pk>/", ArtistSongView.as_view(), name="artist-song"),
    path("albums/<str:pk>/", AlbumSongView.as_view(), name="album-song"),
]
