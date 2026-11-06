from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction

from .models import Student, User

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "autofocus": True}),

    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_username(self):
        return self.cleaned_data["username"].lower()

    def clean(self):
        try:
            return super().clean()
        except forms.ValidationError:
            email = self.cleaned_data.get("username")
            password = self.cleaned_data.get("password")
            user  = User.objects.filter(email__iexact=email, is_active=False).first()
            if user is not None and password and user.check_password(password):
                raise forms.ValidationError(
                    "Account waiting for approval by a Admin.",
                    code="inactive"
                )
            raise

class StudentRegistrationForm(UserCreationForm):
    """This is the sign up form for new accounts. Account will stay inactive untill it has been approved"""

    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name", max_length=80)
    last_name = forms.CharField(label="Last name", max_length=80)
    student_number = forms.CharField(label="Student number", max_length=30)
    qualification = forms.CharField(label="Qualification", max_length=120)
    contact_number = forms.CharField(label="Contact number", max_length=30, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)  #Email address will be the username
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This account name already exists.")
        return email

    def clean_student_number(self):
        number = self.cleaned_data["student_number"].strip()
        if Student.objects.filter(student_number=number).exists():
            raise forms.ValidationError("This is a already registered username.")
        return number

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.role = User.Role.STUDENT
        user.is_active = False
        user.save()
        Student.objects.create(
            user=user,
            student_number=self.cleaned_data["student_number"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            qualification=self.cleaned_data["qualification"],
            contact_number=self.cleaned_data["contact_number"],
        )
        return user