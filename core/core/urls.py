from django.contrib import admin
from django.urls import include, path

apiPrefix = "api/v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{apiPrefix}/users/", include("users.urls")),
]
