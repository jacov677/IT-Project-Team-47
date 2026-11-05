from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import EmailLoginForm
from .models import Coordinator, Mentor, Student, User


@login_required
def index(request):
    context = {
        "total_users": User.objects.count(),
        "total_students": Student.objects.count(),
        "total_coordinators": Coordinator.objects.count(),
        "total_mentors": Mentor.objects.count(),
    }

    return render(request, "accounts/index.html", context)


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = EmailLoginForm
    redirect_authenticated_user = True
