from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Room, RentalRequest
from django.db.models import Case, When, Value, CharField, F


class RoomPaymentHistoryView(LoginRequiredMixin, ListView):
    """
    View to list rooms associated with the logged-in renter's rentals.
    """
    model = Room
    template_name = "renthub/payment_history.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Return a queryset of rooms linked to the logged-in user's rentals."""
        rental_requests = RentalRequest.objects.filter(renter__id=self.request.user.id)
        rooms = Room.objects.filter(rentalrequest__in=rental_requests).annotate(
            status=Case(
                When(rentalrequest__isnull=False, then=F('rentalrequest__status')),
                default=Value(''),
                output_field=CharField(),
            )
        )
        return rooms
