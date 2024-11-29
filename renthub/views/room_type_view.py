from django.views.generic import ListView

from ..models import Room


class RoomTypeView(ListView):
    """
    View for displaying rooms of a specific type.
    """
    model = Room
    template_name = "renthub/roomtype.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Retrieve the rooms that match the specified room type from the URL."""
        room_type = self.kwargs['room_type']
        rooms = Room.objects.filter(room_type__type_name=room_type).order_by('room_number')
        available_rooms = [room for room in rooms if room.is_available()]
        return available_rooms
