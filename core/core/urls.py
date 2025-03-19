from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(),
)

api_prefix = "api/v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{api_prefix}/users/", include("users.urls")),
    path(f"{api_prefix}/auth/", include("authentication.urls")),
    path(f"{api_prefix}/artists/", include("artists.urls")),
    path(f"{api_prefix}/albums/", include("albums.urls")),
    path(f"{api_prefix}/songs/", include("songs.urls")),
    # Swagger paths
    path(
        "swagger.<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
