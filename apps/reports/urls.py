
from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.index, name="index"),
    path("placements/", views.placement_summary, name="placement_summary"),
    path("students/", views.student_reports, name="student_reports"),
    path("organisations/", views.organisation_reports, name="organisation_reports"),
    path("completion/", views.completion_reports, name="completion_reports"),
]

