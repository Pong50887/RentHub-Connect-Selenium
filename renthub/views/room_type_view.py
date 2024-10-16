from django.views.generic import ListView

from ..models import Room


class RoomTypeView(ListView):
    model = Room
    template_name = "renthub/roomtype.html"
    context_object_name = "rooms"

    def get_queryset(self):
        pass
        # Get the room type from the URL
        room_type = self.kwargs['room_type']
        return Room.objects.filter(room_type__type_name=room_type)
