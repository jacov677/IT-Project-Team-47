from django.shortcuts import render


def index(request):
    """Start page of the Placements module. Replace with the real pages."""
    return render(request, "placements/index.html")
