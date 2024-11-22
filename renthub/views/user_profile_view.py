from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ..models import Renter


class UserProfileView(View):

    def get(self, request, username):
        try:
            renter = Renter.objects.filter(username=username).first()
        except Renter.DoesNotExist:
            return redirect('renthub:home')
        return render(request, 'renthub/user_profile.html', {'renter': renter})
