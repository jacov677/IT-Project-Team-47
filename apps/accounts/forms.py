from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from .models import User


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True, "class": "form-control"}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    error_messages = {
        "invalid_login": "Incorrect email or password.",
        "inactive": "Your account is not active yet. An administrator must approve it first.",
    }

    def clean(self):
        try:
            return super().clean()
        except ValidationError:
            # Django rejects inactive users with the generic message. Show the clearer
            # "not active yet" message, but only when the password is correct.
            email = self.cleaned_data.get("username", "")
            password = self.cleaned_data.get("password", "")
            user = User.objects.filter(email__iexact=email, is_active=False).first()
            if user is not None and user.check_password(password):
                raise ValidationError(self.error_messages["inactive"], code="inactive") from None
            raise


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "role")


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "role", "is_active")
