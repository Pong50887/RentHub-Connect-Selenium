from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from ..models import Renter


class ThaiCitizenshipIDWidget(forms.MultiWidget):
    """
    A custom widget for entering a Thai citizenship ID, which consists of 13 single-character input fields.
    """

    def __init__(self, attrs=None):
        """Initializes the widget with 13 text input fields for the Thai citizenship ID."""
        widgets = [forms.TextInput(attrs={'maxlength': 1, 'style': 'width: 20px; text-align: center;'})
                   for _ in range(13)]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        """
        Decompresses the value into a list of individual characters for each input field.

        :param value: The combined value (string) from the form.
        :return: A list of 13 individual characters or None if the value is empty.
        """
        if value:
            return list(value)
        return [None] * 13

    def value_from_datadict(self, data, files, name):
        """
        Combines the values from the 13 individual input fields into a single string.

        :param data: The form data.
        :param files: The files associated with the form submission.
        :param name: The name of the field.
        :return: A single string representing the Thai citizenship ID.
        """
        values = [data.get(f'{name}_{i}', '') for i in range(13)]
        return ''.join(values)


class RenterSignupForm(UserCreationForm):
    """
    A form for registering a new renter, including their phone number and Thai citizenship ID,
    as well as their account details such as username, email, and password.
    """
    phone_number = forms.CharField(max_length=10, required=True, help_text="Phone number:")
    thai_citizenship_id = forms.CharField(
        label="Thai Citizenship ID",
        widget=ThaiCitizenshipIDWidget(),
        max_length=13,
        help_text="Enter your 13-digit Thai citizenship ID."
    )
    thai_citizenship_id_image = forms.ImageField(
        required=True,
        label="Thai Citizenship ID Image",
        help_text="Upload an image of your Thai citizenship ID for admin to approve your identity.",
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),
    )

    class Meta:
        model = Renter
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone_number', 'thai_citizenship_id', 'thai_citizenship_id_image',
            'password1', 'password2'
        ]

    def clean_thai_citizenship_id(self):
        """
        Validates the Thai citizenship ID, ensuring it is exactly 13 digits long and contains only numbers.

        :return: The valid Thai citizenship ID as a string.
        :raises ValidationError: If the ID is not 13 digits or contains non-digit characters.
        """
        id_parts = self.cleaned_data.get('thai_citizenship_id')
        if id_parts:
            thai_id = ''.join(part for part in id_parts if part)
            if len(thai_id) != 13 or not thai_id.isdigit():
                raise ValidationError("Please enter a valid 13-digit Thai citizenship ID.")
            return thai_id
        raise ValidationError("Please enter a valid 13-digit Thai citizenship ID.")
