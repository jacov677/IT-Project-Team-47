from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """ Only students with a given role can open the view.

    The usage her :
        @role__required(User.Role.COORDINATOR, User.Role>ADMIN)
        def my_view (request):

        not logged in --> redirected to login page
        wrong rule --> 403 forbidden
        Superusers can always open the view

    """

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser or request.user.role in roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper

    return decorator