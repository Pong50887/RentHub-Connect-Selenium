from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from ..models import Renter


class RenterProfileForm(forms.ModelForm):
    """
    Form for users to update their profile information.
    """
    password = forms.CharField(widget=forms.PasswordInput(), label='Current Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm New Password')

    class Meta:
        model = Renter
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'thai_citizenship_id']

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if current_password:
            user = authenticate(username=self.instance.username, password=current_password)
            if not user:
                raise ValidationError("The current password is incorrect.")

        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise ValidationError("The new passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        """
        Save the form data. Updates the user's password if changed.
        """
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user
