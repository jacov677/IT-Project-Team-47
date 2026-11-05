from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import User, Student, Coordinator, Mentor


@login_required
def index(request):
    context = {
        "total_users": User.objects.count(),
        "total_students": Student.objects.count(),
        "total_coordinators": Coordinator.objects.count(),
        "total_mentors": Mentor.objects.count(),
    }

    return render(request, "accounts/index.html", context)

