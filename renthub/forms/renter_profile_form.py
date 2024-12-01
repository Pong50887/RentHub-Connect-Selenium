from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from ..models import Renter


class RenterProfileForm(forms.ModelForm):
    """
    Form for users to update their profile information.
    """
    password = forms.CharField(widget=forms.PasswordInput(), label='Current Password', required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label='New Password', required=False,
                                    validators=[validate_password])
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm New Password', required=False,
                                    validators=[validate_password])

    class Meta:
        model = Renter
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'thai_citizenship_id',
                  'thai_citizenship_id_image']
        widgets = {
            'thai_citizenship_id_image': forms.ClearableFileInput(attrs={'accept': 'image/*'})
        }

    def clean(self):
        """
        Clean the form data by validating the current password and checking if the new passwords match.
        """
        cleaned_data = super().clean()
        current_password = cleaned_data.get('password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        thai_citizenship_id_image = cleaned_data.get('thai_citizenship_id_image')

        if current_password:
            user = authenticate(username=self.instance.username, password=current_password)
            if not user:
                self.add_error('password', "The current password is incorrect.")

        if new_password1 or new_password2:
            if new_password1 != new_password2:
                self.add_error('new_password2', "The new passwords do not match.")

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
