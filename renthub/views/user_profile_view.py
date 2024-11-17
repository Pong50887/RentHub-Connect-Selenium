from django.shortcuts import get_object_or_404, render
from django.views import View
from ..models import Renter


class UserProfileView(View):
    def get(self, request, user_id):
        renter = get_object_or_404(Renter, id=user_id)

        return render(request, 'renthub/user_profile.html', {'renter': renter})
