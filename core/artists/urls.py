from django.urls import path

from artists.views import ArtistListView

urlpatterns = [
    path("", ArtistListView.as_view(), name="aritst-list"),
    # path("<str:pk>/", ArtistListView.as_view(), name="aritst-list"),
]
