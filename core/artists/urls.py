from django.urls import path

from artists.views import ArtistDetailView, ArtistListView, ManagerArtistView

urlpatterns = [
    path("<str:pk>/", ArtistDetailView.as_view(), name="aritst-detail"),
    path(
        "managers/<str:manager_id>/",
        ManagerArtistView.as_view(),
        name="manager-artists",
    ),
    path("", ArtistListView.as_view(), name="aritst-list"),
]
