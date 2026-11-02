from django.urls import path

from . import views

app_name = "placements"

urlpatterns = [
    path("", views.index, name="index"),
]
