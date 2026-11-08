
from django.urls import path
from . import views

app_name = "logbook"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:placement_id>/", views.placement_entries, name="placement_entries"),
    path("<int:placement_id>/add/", views.add_entry, name="add_entry"),
    path("<int:placement_id>/entry/<int:entry_id>/delete/", views.delete_entry, name="delete_entry"),
]
