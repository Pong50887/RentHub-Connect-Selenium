from django.views.generic import ListView

from ..models import Room


class RoomListView(ListView):
    """
    View to list all available rooms.
    """
    model = Room
    template_name = "renthub/rental_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Return a queryset of available rooms."""
        return Room.objects.filter(availability=True)
