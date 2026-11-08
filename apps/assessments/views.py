
from django.shortcuts import render

from apps.accounts.decorators import role_required
from apps.accounts.models import User


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def index(request):
    """Display the coordinator assessments dashboard."""
    return render(request, "assessments/index.html")


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def assessment_list(request):
    """Display all student assessments."""
    return render(request, "assessments/assessment_list.html")


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def assessment_detail(request):
    """Display individual assessment details."""
    return render(request, "assessments/assessment_detail.html")


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def result_capture(request):
    """Display the final assessment result capture form."""
    return render(request, "assessments/result_capture.html")


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def assessment_history(request):
    """Display previously captured assessment results."""
    return render(request, "assessments/assessment_history.html")
