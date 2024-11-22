from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.utils import timezone
from datetime import timedelta

from ..models import Room, Rental, Renter
from ..utils import get_room_images


class RoomDetailView(DetailView):
    """
    Display the details of a specific room.
    """
    model = Room
    template_name = "renthub/room.html"
    context_object_name = "room"

    def get_object(self, queryset=None):
        """Retrieve the room object based on the room number."""
        room_number = self.kwargs.get("room_number")
        room = get_object_or_404(Room, room_number=room_number)

        return room

    def get(self, request, *args, **kwargs):
        """Handle GET requests for room details."""
        room_number = self.kwargs.get("room_number")
        room = get_object_or_404(Room, room_number=room_number)
        if not room.is_available():
            messages.error(self.request, "The room is not available.")
            return redirect('renthub:home')

        try:
            self.get_object()
        except Http404:
            return HttpResponseRedirect(reverse("renthub:home"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add extra context data to the template."""
        context = super().get_context_data(**kwargs)
        room = self.get_object()

        if room.room_image:
            context["room_images"] = room.room_image.all()

        try:
            renter = Renter.objects.get(id=self.request.user.id)
        except Renter.DoesNotExist:
            renter = None

        if renter:
            context["rental"] = Rental.objects.filter(renter=renter, room=room,
                                                      start_date__lt=timezone.now() + timedelta(days=30),
                                                      end_date__gt=timezone.now()).first()

        return context
