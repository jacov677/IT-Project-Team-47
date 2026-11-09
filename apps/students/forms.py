from django import forms
from django.contrib.auth import get_user_model

from apps.accounts.models import Student
from .models import Application, StudentPortalProfile

User = get_user_model()
MAX_CV_MB = 5


class StyledFormMixin:
    """Adds the CSS class used by the blue-and-white theme to every widget."""

    def _style(self):
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-control")


class UserUpdateForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self._style()

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Another account already uses this email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # accounts app uses the email as the username
        if commit:
            user.save()
            # Keep the name on the Student record the same as on the login account.
            Student.objects.filter(user=user).update(first_name=user.first_name, last_name=user.last_name)
        return user


class StudentDetailsForm(StyledFormMixin, forms.ModelForm):
    """The parts of accounts.Student a student may change themselves."""

    class Meta:
        model = Student
        fields = ("qualification", "contact_number")
        labels = {"qualification": "Programme", "contact_number": "Phone"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()


class ProfileUpdateForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = StudentPortalProfile
        fields = ("year_of_study", "skills", "bio", "cv")
        widgets = {"skills": forms.Textarea(attrs={"rows": 2}), "bio": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    def clean_cv(self):
        cv = self.cleaned_data.get("cv")
        if cv and hasattr(cv, "size"):
            if not cv.name.lower().endswith(".pdf"):
                raise forms.ValidationError("Please upload your CV as a PDF.")
            if cv.size > MAX_CV_MB * 1024 * 1024:
                raise forms.ValidationError(f"CV must be smaller than {MAX_CV_MB} MB.")
        return cv


class ApplicationForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Application
        fields = ("cover_letter",)
        widgets = {"cover_letter": forms.Textarea(attrs={
            "rows": 7, "placeholder": "Tell the organisation why you are a good fit…"})}
        labels = {"cover_letter": "Motivation / cover letter"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    def clean_cover_letter(self):
        text = self.cleaned_data["cover_letter"].strip()
        if len(text) < 30:
            raise forms.ValidationError("Please write at least a couple of sentences (30+ characters).")
        return text
