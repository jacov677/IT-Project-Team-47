from django.shortcuts import render


def index(request):
    """Start page of the Accounts module. Replace with the real pages."""
    return render(request, "accounts/index.html")
