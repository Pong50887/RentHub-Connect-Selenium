from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import DetailView

from ..models import Room, Rental


class RoomDetailView(DetailView):
    model = Room
    template_name = "renthub/rental.html"
    context_object_name = "room"

    def get_object(self, queryset=None):
        room_number = self.kwargs.get("room_number")
        room = get_object_or_404(Room, room_number=room_number)
        return room

    def get(self, request, *args, **kwargs):
        try:
            room = self.get_object()
        except Http404:
            return HttpResponseRedirect(reverse("renthub:home"))

        if not room.availability:
            if Rental.objects.filter(room=room).exists():
                messages.info(request, "This room is taken.")
            else:
                messages.error(request, "This room is currently unavailable.")
            return HttpResponseRedirect(reverse("renthub:home"))

        return super().get(request, *args, **kwargs)
