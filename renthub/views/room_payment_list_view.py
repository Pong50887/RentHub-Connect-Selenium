from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Room, Rental
from django.db.models import F
from django.utils import timezone
from datetime import timedelta

from ..utils import Status


class RoomPaymentListView(LoginRequiredMixin, ListView):
    """
    View to list rooms associated with the logged-in renter's rentals.
    """
    model = Room
    template_name = "renthub/payment_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Return a queryset of rooms linked to the logged-in user's rentals."""
        rentals = Rental.objects.filter(renter__id=self.request.user.id,
                                        start_date__lt=timezone.now() + timedelta(days=30),
                                        end_date__gt=timezone.now()).exclude(status=Status.reject)
        rooms_with_rentals = Room.objects.filter(
            rental__in=rentals
        ).annotate(
            status=F('rental__status')
        )

        return rooms_with_rentals
