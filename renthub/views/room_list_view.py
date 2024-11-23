from django.views.generic import ListView
from ..models import Room, RoomType


class RoomListView(ListView):
    """
    A view that displays a list of rental rooms.
    """
    model = Room
    template_name = "renthub/room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Retrieve and filter the list of rooms based on user input."""
        rooms = Room.objects.all().order_by("room_number")
        search_entry = self.request.GET.get("search", "")
        selected_room_type = self.request.GET.get("room_type", "")
        sort_price_option = self.request.GET.get("sort", "")

        available_rooms = []
        for room in rooms:
            if room.is_available():
                available_rooms.append(room.id)
        rooms = rooms.filter(pk__in=available_rooms)

        if search_entry:
            rooms = (rooms.filter(room_number__icontains=search_entry)
                     | rooms.filter(room_type__type_name__icontains=search_entry)
                     | rooms.filter(room_type__description__icontains=search_entry)
                     | rooms.filter(room_type__ideal_for__icontains=search_entry)
                     | rooms.filter(room_type__type_name__icontains=search_entry)
                     | rooms.filter(room_type__features__name__icontains=search_entry)
                     | rooms.filter(detail__icontains=search_entry)).distinct()

        if selected_room_type:
            rooms = rooms.filter(room_type__id=selected_room_type)

        if sort_price_option == "price_asc":
            rooms = rooms.order_by("price", "room_number")
        elif sort_price_option == "price_desc":
            rooms = rooms.order_by("-price", "room_number")

        return rooms

    def get_context_data(self, **kwargs):
        """Add additional context to the template."""
        context = super().get_context_data(**kwargs)
        context.update({
            "search_entry": self.request.GET.get("search", ""),
            "selected_room_type": self.request.GET.get("room_type", ""),
            "sort_price_option": self.request.GET.get("sort", ""),
            "room_types": RoomType.objects.all(),
            "search_results_exist": bool(self.get_queryset())
        })
        return context
