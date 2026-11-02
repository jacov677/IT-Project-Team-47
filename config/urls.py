from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "WIL Placement System administration"
admin.site.site_title = "WIL Placement System"
admin.site.index_title = "System management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("placements/", include("apps.placements.urls")),
    path("logbook/", include("apps.logbook.urls")),
    path("assessments/", include("apps.assessments.urls")),
    path("", include("apps.core.urls")),
]
# Note: uploaded documents are deliberately NOT served via MEDIA_URL.
# Use placements:download_document, which checks permissions first.
