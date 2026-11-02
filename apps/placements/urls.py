from django.urls import path

from . import views

app_name = "placements"

urlpatterns = [
    path("<int:pk>/", views.placement_detail, name="detail"),
    path("documents/<int:pk>/download/", views.download_document, name="download_document"),
    # TODO (placements module): create placement, coordinator approve/reject, upload document.
]
