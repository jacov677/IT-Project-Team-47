from django.shortcuts import render


MODULES = [
    ("accounts:index", "Accounts", "Login, registration, roles and profiles"),
    ("organisations:index", "Organisations", "Host organisations"),
    ("placements:index", "Placements", "Placement requests, approval and documents"),
    ("logbook:index", "Logbook", "Logbook entries and mentor sign-off"),
    ("assessments:index", "Assessments", "Mentor evaluations and final results"),
    ("reports:index", "Reports", "Coordinator reports and audit log"),
]


def home(request):
    return render(request, "core/home.html", {"modules": MODULES})


def audit_log(request):
    return render(request, "core/audit_log.html")