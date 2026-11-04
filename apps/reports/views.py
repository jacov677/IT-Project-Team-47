
from django.shortcuts import render


def index(request):
    return render(request, "reports/index.html")


def placement_summary(request):
    return render(request, "reports/placement_summary.html")


def student_reports(request):
    return render(request, "reports/student_reports.html")


def organisation_reports(request):
    return render(request, "reports/organisation_reports.html")


def completion_reports(request):
    return render(request, "reports/completion_reports.html")
