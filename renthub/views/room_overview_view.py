from django.views.generic import TemplateView
from ..models import Room
from ..utils import Status


class RoomOverviewView(TemplateView):
    template_name = "renthub/room_overview.html"

    def get_context_data(self, **kwargs):
        """
        Pass context data for room overview, including room availability and renter details.
        """
        context = super().get_context_data(**kwargs)

        # Fetch all rooms and prefetch related rentals
        rooms = Room.objects.prefetch_related('rental_set').order_by('room_number')

        room_data = []
        for room in rooms:
            # Check if the room has an active rental
            active_rental = room.rental_set.filter(status__in=[Status.wait, Status.approve]).first()
            room_data.append({
                'room_number': room.room_number,
                'is_available': active_rental is None,  # Available if no active rental
                'renter_name': active_rental.renter.username if active_rental else None,
                'renter_id': active_rental.renter.id if active_rental else None,  # Pass renter ID for linking
                'is_paid': active_rental.is_paid if active_rental else None,  # Include paid status
            })

        context['rooms'] = room_data
        return context
