"""Server-side role checks (section 4.1: hiding a button is not authorisation).

Function views:

    @role_required(Role.COORDINATOR)
    def approve(request, pk): ...

Class-based views:

    class ApproveView(RoleRequiredMixin, View):
        allowed_roles = [Role.COORDINATOR]
"""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied("You are not authorised to access this page.")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role not in self.allowed_roles:
            raise PermissionDenied("You are not authorised to access this page.")
        return super().dispatch(request, *args, **kwargs)
