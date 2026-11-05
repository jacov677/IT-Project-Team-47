
from django import forms
from .models import LogbookEntry


# Form for students to record their daily activities
class LogbookEntryForm(forms.ModelForm):
    class Meta:
        model = LogbookEntry
        fields = [
            "entry_date",
            "activities",
            "hours_worked",
            "supervisor_comments",
        ]

        widgets = {
            "entry_date": forms.DateInput(attrs={"type": "date"}),
            "activities": forms.Textarea(attrs={"rows": 4}),
            "supervisor_comments": forms.Textarea(attrs={"rows": 3}),
        }
