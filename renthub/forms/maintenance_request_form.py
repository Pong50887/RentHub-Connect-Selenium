from django import forms
from django.utils import timezone

from ..models import MaintenanceRequest


class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['title', 'request_message']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'request_message': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': 'Issue Title',
            'request_message': 'Describe the problem',
        }

    def save(self, rental, commit=True):
        maintenance_request = super().save(commit=False)
        maintenance_request.rental = rental
        maintenance_request.date_requested = timezone.now()
        if commit:
            maintenance_request.save()
        return maintenance_request
