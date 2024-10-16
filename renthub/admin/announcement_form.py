from django import forms

from ..models import Announcement


class AnnouncementForm(forms.ModelForm):
    """
    Form for creating and updating Announcement objects.
    """
    class Meta:
        model = Announcement
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 10,
                'cols': 80,
                'style': 'resize: both;'
            }),
        }
