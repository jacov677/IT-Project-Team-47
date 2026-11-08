
from django import forms
from .models import Placement, Document


class PlacementForm(forms.ModelForm):
    class Meta:
        model = Placement
        fields = [
            "student",
            "organisation",
            "title",
            "description",
            "start_date",
            "end_date",
            "status",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            "title",
            "document_type",
            "file_path",
        ]
