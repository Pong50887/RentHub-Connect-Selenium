from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
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
        try:
            return Renter.objects.get(id=self.request.user.id)
        except Renter.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        """
        Redirect if the object does not exist.
        """
        obj = self.get_object()
        if obj is None:
            messages.error(request, "Only renter can view profiles.")
            return redirect("renthub:home")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Set Renter.is_valid to False after a successful form submission.
        """
        response = super().form_valid(form)
        renter = self.object
        renter.is_valid = False
        renter.save()
        return response
