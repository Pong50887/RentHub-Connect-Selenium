from django.views.generic import ListView

from ..models import Room


class RoomListView(ListView):
    model = Room
    template_name = "renthub/rental_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.filter(availability=True)
