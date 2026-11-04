from django.shortcuts import render


def index(request):
    """Display the coordinator assessments dashboard."""
    return render(request, "assessments/index.html")


def assessment_list(request):
    """Display all student assessments."""
    return render(request, "assessments/assessment_list.html")


def assessment_detail(request):
    """Display individual assessment details."""
    return render(request, "assessments/assessment_detail.html")


def result_capture(request):
    """Display the final assessment result capture form."""
    return render(request, "assessments/result_capture.html")


def assessment_history(request):
    """Display previously captured assessment results."""
    return render(request, "assessments/assessment_history.html")