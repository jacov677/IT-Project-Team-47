from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from apps.placements.models import Placement
from .models import LogbookEntry
from .forms import LogbookEntryForm


# Show available placements
def index(request):
    placements = Placement.objects.all().order_by("-created_at")

    return render(request, "logbook/index.html", {
        "placements": placements,
    })


# Display entries for a selected placement
def placement_entries(request, placement_id):
    placement = get_object_or_404(Placement, pk=placement_id)

    entries = LogbookEntry.objects.filter(
        placement=placement
    ).order_by("-entry_date")

    return render(request, "logbook/index.html", {
        "placement": placement,
        "entries": entries,
    })


# Add a new logbook entry
def add_entry(request, placement_id):
    placement = get_object_or_404(Placement, pk=placement_id)

    if request.method == "POST":
        form = LogbookEntryForm(request.POST)

        if form.is_valid():
            entry = form.save(commit=False)
            entry.placement = placement
            entry.save()

            messages.success(request, "Logbook entry saved successfully!")
            return redirect("logbook:placement_entries", placement_id=placement.pk)

    else:
        form = LogbookEntryForm()

    return render(request, "logbook/add_entry.html", {
        "form": form,
        "placement": placement,
    })

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