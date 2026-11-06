from django import forms
from .models import PlacementOpportunity, HostOrganisation

class PlacementOpportunityForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['organisation'].queryset = HostOrganisation.objects.filter(owner=user)
    class Meta:
        model = PlacementOpportunity
        fields = ['organisation', 'title', 'description', 'slots_available', 'closing_date']
        widgets = {
            'closing_date': forms.DateInput(attrs={'type': 'date'}),
        }