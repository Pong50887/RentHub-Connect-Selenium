from django import forms
from django.utils import timezone

from ..models import MaintenanceRequest


class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['title', 'request_message']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','maxlength': '100'}),
            'request_message': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '1000'}),
        }

        labels = {
            'title': 'Issue Title',
            'request_message': 'Describe the problem',
        }

    def save(self, rental=None, commit=True):
        """
        Save the maintenance request, associating it with a rental if provided.
        """
        maintenance_request = super().save(commit=False)
        if rental:
            maintenance_request.rental = rental
        elif not maintenance_request.rental:
            raise ValueError("A rental instance must be provided to save the maintenance request.")

        maintenance_request.date_requested = timezone.now()

        if commit:
            maintenance_request.save()
        return maintenance_request
