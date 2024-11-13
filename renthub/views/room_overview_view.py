from django.views.generic import TemplateView
from ..models import Room
from ..utils import Status


class RoomOverviewView(TemplateView):
    template_name = "renthub/room_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        rooms = Room.objects.all()
        room_data = [
            {
                'room_number': room.room_number,
                'is_available': room.is_available(),
                'renter_name': room.rental_set.filter(status__in=[Status.wait, Status.approve]).first().renter.username
                if not room.is_available() else None
            }
            for room in rooms
        ]
        context['rooms'] = room_data
        return context
