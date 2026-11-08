
from django.shortcuts import render

from apps.accounts.decorators import role_required
from apps.accounts.models import User


MODULES = [
    ("accounts:index", "Accounts", "Login, registration, roles and profiles"),
    ("organisations:org_dashboard", "Organisations", "Host organisations"),
    ("placements:index", "Placements", "Placement requests, approval and documents"),
    ("logbook:index", "Logbook", "Logbook entries and mentor sign-off"),
    ("assessments:index", "Assessments", "Mentor evaluations and final results"),
    ("reports:index", "Reports", "Coordinator reports and audit log"),
]


def home(request):
    return render(request, "core/home.html", {"modules": MODULES})


@role_required(User.Role.ADMIN)
def audit_log(request):
    return render(request, "core/audit_log.html")


def settings_page(request):
    return render(request, "core/settings.html")
