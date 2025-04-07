from django.urls import path

from .views import (
    AdminMonthlyStatsView,
    AdminStatsView,
    ManagerStatsView,
    MonthlyStatsView,
)

urlpatterns = [
    path("managers/<str:pk>/", ManagerStatsView.as_view(), name="manager-stats"),
    path(
        "managers/<str:pk>/monthly/songs/",
        MonthlyStatsView.as_view(),
        name="monthly-manager-stats",
    ),
    path("admin/", AdminStatsView.as_view(), name="admin-stats"),
    path(
        "admin/monthly/songs/",
        AdminMonthlyStatsView.as_view(),
        name="monthly-admin-stats",
    ),
]
