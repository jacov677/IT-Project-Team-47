from django.shortcuts import render


def index(request):
    """Start page of the Assessments module. Replace with the real pages."""
    return render(request, "assessments/index.html")
