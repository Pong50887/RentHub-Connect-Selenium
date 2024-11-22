from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Renter


class UserProfileView(LoginRequiredMixin, View):
    """
    View to display a user's profile.
    Only accessible to superusers.
    """

    def get(self, request, username):
        # Check if the user is a superuser
        if not request.user.is_superuser:
            return redirect('renthub:home')

        # Retrieve the renter's profile
        renter = get_object_or_404(Renter, username=username)
        return render(request, 'renthub/user_profile.html', {'renter': renter})
