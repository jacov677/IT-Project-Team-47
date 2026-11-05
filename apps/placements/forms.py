
from django import forms
from .models import Placement, Document


# Form for adding and updating student placements
class PlacementForm(forms.ModelForm):
    class Meta:
        model = Placement
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


# Form for adding placement documents
from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            "document_name",
            "document_type",
            "file",
        ]





