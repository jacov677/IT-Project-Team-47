from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailBackend(ModelBackend):
    """Log in with email address and password instead of username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get("email", username)
        if not email or not password:
            return None
        try:
            user = User.objects.get(email__iexact=email)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            User().set_password(password)  # same timing as a real check
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
