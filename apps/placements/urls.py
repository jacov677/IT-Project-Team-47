from django.urls import path

from . import views

app_name = "placements"

urlpatterns = [
    path("", views.index, name="index"),
    path("manage/", views.placement_list, name="placement_list"),
    path("details/", views.placement_detail, name="placement_detail"),
path("create/", views.placement_create, name="placement_create"),
path("documents/", views.document_list, name="document_list"),
]

