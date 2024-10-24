from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import DetailView

from ..models import Room, Rental, RentalRequest, Renter
from ..utils import Status

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

        if not room.availability:
            if Rental.objects.filter(room=room).exists():
                messages.info(request, "This room is already taken.")
            else:
                messages.error(request, "This room is currently unavailable.")
            return HttpResponseRedirect(reverse("renthub:home"))

        try:
            renter = Renter.objects.get(id=self.request.user.id)
        except Renter.DoesNotExist:
            renter = None

        latest_request = RentalRequest.objects.filter(renter=renter, room=room).order_by('-id').first()
        if latest_request:
            if latest_request.status != Status.reject:
                messages.info(request, "This room is already taken.")
                return HttpResponseRedirect(reverse("renthub:home"))

        if RentalRequest.objects.filter(room=room).exclude(renter=renter).exists():
            messages.info(request, "This room is already taken.")
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
            try:
                context["rental"] = Rental.objects.filter(renter=renter, room=room).exists()
            except Rental.DoesNotExist:
                pass
            try:
                context["rental_request"] = RentalRequest.objects.filter(renter=renter, room=room).exists()
                latest_request = RentalRequest.objects.filter(renter=renter, room=room).order_by('-id').first()
                if latest_request:
                    context['latest_request'] = latest_request
            except RentalRequest.DoesNotExist:
                pass

        return context