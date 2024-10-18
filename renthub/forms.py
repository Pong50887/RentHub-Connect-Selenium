from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from renthub.models import Renter


class RenterSignupForm(UserCreationForm):
    """
    Form for registering a new renter.
    """
    phone_number = forms.CharField(max_length=10, required=True, help_text="Phone number:")

    class Meta:
        model = Renter
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'phone_number']
