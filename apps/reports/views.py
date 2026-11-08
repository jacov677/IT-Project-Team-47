

from django.shortcuts import render

from apps.accounts.decorators import role_required
from apps.accounts.models import User


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def index(request):
    return render(request, "reports/index.html")


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def placement_summary(request):
    return render(request, "reports/placement_summary.html")


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def student_reports(request):
    return render(request, "reports/student_reports.html")


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def organisation_reports(request):
    return render(request, "reports/organisation_reports.html")


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def completion_reports(request):
    return render(request, "reports/completion_reports.html")
