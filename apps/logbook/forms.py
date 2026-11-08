
from django import forms
from .models import LogbookEntry


# Form for students to record their daily activities
class LogbookEntryForm(forms.ModelForm):
    class Meta:
        model = LogbookEntry
        fields = [
            "date",
            "hours_worked",
            "activities",
            "skills_learned",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "activities": forms.Textarea(attrs={"rows": 4}),
            "skills_learned": forms.Textarea(attrs={"rows": 3}),
        }
