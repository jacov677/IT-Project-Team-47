from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import EmailLoginForm, StudentRegistrationForm
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

class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = StudentRegistrationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "Registration successful. After a administrator admids and verifies your account,you will able to log in.",
        )
        return super().form_valid(form)


# Where each role lands after logging in.
ROLE_HOME = {
    User.Role.STUDENT: "placements:index",
    User.Role.COORDINATOR: "placements:index",
    User.Role.MENTOR: "logbook:index",
    User.Role.EMPLOYER: "organisations:index",
    User.Role.ADMIN: "admin:index",
}


@login_required
def dashboard(request):
    """Send the logged-in user to the start page for their role."""
    if request.user.is_superuser:
        return redirect("admin:index")
    if request.user.role == User.Role.ADMIN:
        return redirect("admin:index" if request.user.is_staff else "core:home")
    return redirect(ROLE_HOME.get(request.user.role, "core:home"))
