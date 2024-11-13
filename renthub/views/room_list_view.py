from django.views.generic import ListView
from ..models import Room, RoomType
from datetime import datetime


class RoomListView(ListView):
    """
    A view that displays a list of rental rooms.
    """
    model = Room
    template_name = "renthub/room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Retrieve and filter the list of rooms based on user input."""
        rooms = Room.objects.all()
        search_entry = self.request.GET.get("search", "")
        selected_room_type = self.request.GET.get("room_type", "")
        sort_price_option = self.request.GET.get("sort", "")
        start_month = self.request.GET.get("start_month")
        end_month = self.request.GET.get("end_month")

        start_date = datetime.strptime(start_month, "%Y-%m") if start_month else None
        end_date = datetime.strptime(end_month, "%Y-%m") if end_month else None

        available_rooms = []

        if not start_date and not end_date:
            for room in rooms:
                if room.is_available:
                    available_rooms.append(room.id)
            return rooms.filter(pk__in=available_rooms)

        if search_entry:
            rooms = (rooms.filter(room_number__icontains=search_entry)
                     | rooms.filter(room_type__type_name__icontains=search_entry)
                     | rooms.filter(detail__icontains=search_entry))

        if selected_room_type:
            rooms = rooms.filter(room_type__id=selected_room_type)

        for room in rooms:
            if room.is_available():
                available_rooms.append(room.id)
        rooms = rooms.filter(pk__in=available_rooms)

        if sort_price_option == "price_asc":
            rooms = rooms.order_by("price")
        elif sort_price_option == "price_desc":
            rooms = rooms.order_by("-price")

        return rooms

    def get_context_data(self, **kwargs):
        """Add additional context to the template."""
        context = super().get_context_data(**kwargs)
        context.update({
            "search_entry": self.request.GET.get("search", ""),
            "selected_room_type": self.request.GET.get("room_type", ""),
            "sort_price_option": self.request.GET.get("sort", ""),
            "room_types": RoomType.objects.all(),
            "search_results_exist": bool(self.get_queryset()),
            "start_date": self.request.GET.get("start_month"),
            "end_date": self.request.GET.get("end_month")
        })
        return context
