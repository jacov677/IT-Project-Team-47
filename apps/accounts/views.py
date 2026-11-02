from django.contrib.auth import views as auth_views
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from apps.audit.services import log_action

from .forms import EmailLoginForm


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = EmailLoginForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass


@receiver(user_logged_in)
def audit_login(sender, request, user, **kwargs):
    log_action(user, "Login", user)
