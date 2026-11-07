from django import forms
from .models import PlacementOpportunity


class PlacementOpportunityForm(forms.ModelForm):
    class Meta:
        model = PlacementOpportunity
        fields = ['title', 'description', 'slots_available', 'closing_date']
        widgets = {
            'closing_date': forms.DateInput(attrs={'type': 'date'}),
        }