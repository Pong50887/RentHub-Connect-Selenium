from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Room, Rental, RentalRequest
from django.db.models import Case, When, Value, CharField, F

class RoomPaymentListView(LoginRequiredMixin, ListView):
    """
    View to list rooms associated with the logged-in renter's rentals.
    """
    model = Room
    template_name = "renthub/payment_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Return a queryset of rooms linked to the logged-in user's rentals."""
        rental_requests = RentalRequest.objects.filter(renter__id=self.request.user.id, status='wait')
        rentals = Rental.objects.filter(renter__id=self.request.user.id)
        rooms_with_rentals = Room.objects.filter(
            rental__in=rentals
        ).annotate(
            status=Value('successful', output_field=CharField())
        )

        rooms_with_requests = Room.objects.filter(
            rentalrequest__in=rental_requests
        ).annotate(
            status=F('rentalrequest__status')
        )

        combined_rooms = rooms_with_rentals.union(rooms_with_requests)

        return combined_rooms
