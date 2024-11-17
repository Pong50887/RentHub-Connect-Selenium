from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import RenterProfileForm
from ..models import Renter


class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    """
    Class-based view for updating user profile information and changing password.
    """
    model = Renter
    form_class = RenterProfileForm
    template_name = 'renthub/profile_settings.html'
    success_url = reverse_lazy('renthub:profile_settings')

    def get_object(self, **kwargs):
        """
        Ensure the current logged-in user is the one being edited.
        """
        return Renter.objects.get(id=self.request.user.id)
