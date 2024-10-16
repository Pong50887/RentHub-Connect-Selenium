from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Room, Rental


class RoomPaymentListView(LoginRequiredMixin, ListView):
    """
    View to list rooms associated with the logged-in renter's rentals.
    """
    model = Room
    template_name = "renthub/payment_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Return a queryset of rooms linked to the logged-in user's rentals."""
        rentals = Rental.objects.filter(renter__id=self.request.user.id)
        return Room.objects.filter(rental__in=rentals)
