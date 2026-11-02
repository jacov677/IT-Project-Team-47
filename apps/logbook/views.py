from django.shortcuts import render


def index(request):
    """Start page of the Logbook module. Replace with the real pages."""
    return render(request, "logbook/index.html")
