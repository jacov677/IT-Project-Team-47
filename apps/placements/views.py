

from django.shortcuts import render


def index(request):
    """Display the coordinator dashboard."""
    return render(request, "placements/index.html")


def placement_list(request):
    """Display all workplace placements."""
    return render(request, "placements/placement_list.html")


def placement_detail(request):
    """Display placement details."""
    return render(request, "placements/placement_detail.html")


def placement_create(request):
    """Display the placement creation form."""
    return render(request, "placements/placement_form.html")


def document_list(request):
    """Display placement documents."""
    return render(request, "placements/document_list.html")
