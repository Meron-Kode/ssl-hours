from django import forms
from .models import VolunteerLog


class VolunteerLogForm(forms.ModelForm):
    class Meta:
        model = VolunteerLog
        fields = [
            'organization_name',
            'volunteer_date',
            'hours_worked',
            'supervisor_name',
            'supervisor_email',
            'reflection',
        ]
        widgets = {
            'volunteer_date': forms.DateInput(attrs={'type': 'date'}),
            'reflection': forms.Textarea(attrs={'rows': 4}),
        }
