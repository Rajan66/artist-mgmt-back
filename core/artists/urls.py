from django.urls import path

from artists.views import ArtistDetailView, ArtistListView

urlpatterns = [
    path("", ArtistListView.as_view(), name="aritst-list"),
    path("<str:pk>/", ArtistDetailView.as_view(), name="aritst-detail"),
]
