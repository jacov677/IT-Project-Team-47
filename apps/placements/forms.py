


from django import forms

from apps.accounts.models import Student, Mentor
from apps.organisations.models import HostOrganization

from .models import Placement, Document


class PlacementForm(forms.ModelForm):

    class Meta:
        model = Placement
        fields = [
            "student",
            "organisation",
            "mentor",
            "title",
            "description",
            "start_date",
            "end_date",
        ]

        widgets = {
            "student": forms.Select(attrs={"class": "form-select"}),
            "organisation": forms.Select(attrs={"class": "form-select"}),
            "mentor": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter placement title",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Describe the placement",
            }),
            "start_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "end_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["student"].queryset = Student.objects.select_related(
            "user"
        ).order_by("student_number")

        self.fields["organisation"].queryset = (
            HostOrganization.objects.filter(is_active=True)
            .order_by("organisation_name")
        )

        self.fields["mentor"].queryset = Mentor.objects.select_related(
            "organisation"
        ).order_by("first_name", "last_name")

        self.fields["mentor"].required = False

        self.fields["student"].empty_label = "Select student"
        self.fields["organisation"].empty_label = "Select host organisation"
        self.fields["mentor"].empty_label = "Select workplace mentor (optional)"

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        organisation = cleaned_data.get("organisation")
        mentor = cleaned_data.get("mentor")

        if start_date and end_date and end_date <= start_date:
            self.add_error(
                "end_date",
                "The end date must be after the start date.",
            )

        if (
            mentor
            and organisation
            and mentor.organisation_id != organisation.organisation_id
        ):
            self.add_error(
                "mentor",
                "The selected mentor must belong to the chosen organisation.",
            )

        return cleaned_data


class DocumentForm(forms.ModelForm):

    placement = forms.ModelChoiceField(
        queryset=Placement.objects.select_related(
            "student",
            "organisation",
        ).order_by("-created_at"),
        required=False,
        label="Placement",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Document
        fields = [
            "title",
            "document_type",
            "file_path",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter document title",
            }),
            "document_type": forms.Select(attrs={
                "class": "form-select",
            }),
            "file_path": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
        }
