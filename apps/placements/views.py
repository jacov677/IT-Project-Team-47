
from django.shortcuts import render, redirect, get_object_or_404
from .models import Placement, Document
from .forms import PlacementForm, DocumentForm


# Main placements page
def index(request):
    placements = Placement.objects.all()

    return render(request, "placements/index.html", {
        "placements": placements
    })


# Add a new placement
def add_placement(request):
    form = PlacementForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("placements:index")

    return render(request, "placements/placement_form.html", {
        "form": form
    })


# View placement details
def placement_detail(request, pk):
    placement = get_object_or_404(Placement, pk=pk)
    documents = placement.documents.all()

    return render(request, "placements/placement_detail.html", {
        "placement": placement,
        "documents": documents
    })


# Upload and view documents for a placement
def add_document(request, pk):
    placement = get_object_or_404(Placement, pk=pk)
    documents = placement.documents.all()

    form = DocumentForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST" and form.is_valid():
        document = form.save(commit=False)
        document.placement = placement
        document.save()

        return redirect("placements:add_document", pk=pk)

    return render(request, "placements/documents.html", {
        "form": form,
        "placement": placement,
        "documents": documents
    })
