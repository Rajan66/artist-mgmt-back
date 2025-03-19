from django.urls import path

from songs.views import SongDetailView, SongListView

urlpatterns = [
    # Songs
    path("", SongListView.as_view(), name="song-list"),
    path("<str:pk>/", SongDetailView.as_view(), name="song-detail"),
]
