from django.urls import path

from albums.views.album import AlbumDetailView, AlbumListView

urlpatterns = [
    path("<str:album_id>/", AlbumDetailView.as_view(), name="album-detail"),
    path("", AlbumListView.as_view(), name="album-list"),
]
