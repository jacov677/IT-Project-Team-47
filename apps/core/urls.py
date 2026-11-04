from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("audit-log/", views.audit_log, name="audit_log"),
]
