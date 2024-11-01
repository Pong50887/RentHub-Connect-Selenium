from dateutil.relativedelta import relativedelta
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView
from django.utils import timezone
from datetime import timedelta

from ..models import Room, Rental, Renter


class RoomDetailView(DetailView):
    """
    Display the details of a specific room.
    """
    model = Room
    template_name = "renthub/rental.html"
    context_object_name = "room"

    def get_object(self, queryset=None):
        """Retrieve the room object based on the room number."""
        room_number = self.kwargs.get("room_number")
        room = get_object_or_404(Room, room_number=room_number)
        return room

    def get(self, request, *args, **kwargs):
        """Handle GET requests for room details."""
        try:
            room = self.get_object()
        except Http404:
            return HttpResponseRedirect(reverse("renthub:home"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add extra context data to the template."""
        context = super().get_context_data(**kwargs)
        room = self.get_object()

        try:
            renter = Renter.objects.get(id=self.request.user.id)
        except Renter.DoesNotExist:
            renter = None

        if renter:
            context["rental"] = Rental.objects.filter(renter=renter, room=room,
                                                      start_date__lt=timezone.now() + timedelta(days=30),
                                                      end_date__gt=timezone.now()).first()

        rentals = Rental.objects.filter(room=room)
        occupied_months = []

        for rental in rentals:
            start = rental.start_date
            end = rental.end_date
            current = start

            while current <= end:
                occupied_months.append(current.strftime("%Y-%m"))
                if current.month == 12:
                    current = current.replace(year=current.year + 1, month=1, day=1)
                else:
                    current = current + relativedelta(months=1)
                if current.day > 28:
                        current = current + relativedelta(day=31)
                        current = current.replace(day=1)

        context["occupied_months"] = occupied_months

        return context
