from django.shortcuts import render


def index(request):
    """Start page of the Reports module. Replace with the real pages."""
    return render(request, "reports/index.html")
