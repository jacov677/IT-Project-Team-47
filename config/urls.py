from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("organisations/", include("apps.organisations.urls")),
    path("placements/", include("apps.placements.urls")),
    path("logbook/", include("apps.logbook.urls")),
    path("assessments/", include("apps.assessments.urls")),
    path("reports/", include("apps.reports.urls")),
    path("", include("apps.core.urls")),
]
