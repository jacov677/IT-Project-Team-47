
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

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

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
