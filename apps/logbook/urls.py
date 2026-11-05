from django.urls import path
from . import views

app_name = "logbook"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:placement_id>/", views.placement_entries, name="placement_entries"),
    path("<int:placement_id>/add/", views.add_entry, name="add_entry"),
    path("<int:placement_id>/entry/<int:entry_id>/delete/", views.delete_entry, name="delete_entry"),
]

# Delete a logbook entry
def delete_entry(request, placement_id, entry_id):
    placement = get_object_or_404(Placement, pk=placement_id)

    entry = get_object_or_404(
        LogbookEntry,
        pk=entry_id,
        placement=placement
    )

    if request.method == "POST":
        entry.delete()
        messages.success(request, "Logbook entry deleted successfully!")
        return redirect("logbook:placement_entries", placement_id=placement.pk)

    return redirect("logbook:placement_entries", placement_id=placement.pk)