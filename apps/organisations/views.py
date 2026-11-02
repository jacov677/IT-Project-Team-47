from django.shortcuts import render


def index(request):
    """Start page of the Organisations module. Replace with the real pages."""
    return render(request, "organisations/index.html")
