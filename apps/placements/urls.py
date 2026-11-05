from django.urls import path

from . import views

app_name = "placements"

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add_placement, name="add_placement"),
    path("<int:pk>/", views.placement_detail, name="placement_detail"),
    path("<int:pk>/documents/add/", views.add_document, name="add_document"),
]