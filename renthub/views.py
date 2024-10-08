from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Room, Rental, Renter
from django.contrib import messages
from django.views.generic import ListView, DetailView


class HomeView(ListView):
    model = Room
    template_name = "renthub/home.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.filter(availability=True)

class RoomDetailView(DetailView):
    model = Room
    template_name = "renthub/rental.html"
    context_object_name = "room"

    def get(self, request, *args, **kwargs):
        room = self.get_object()
        if not room.availability:
            return HttpResponseRedirect(reverse("renthub:home"))
        return super().get(request, *args, **kwargs)

class RoomPaymentView(DetailView):
    model = Room
    template_name = "renthub/payment.html"
    context_object_name = "room"

    def get(self, request, *args, **kwargs):
        room = self.get_object()
        if not room.availability:
            messages.error(request, f"The room {room} is currently unavailable.")
            return HttpResponseRedirect(reverse("renthub:home"))
        return super().get(request, *args, **kwargs)

def submit_payment(request, room_id):
    room = Room.objects.get(id=room_id)
    user = request.user
    # try:
    #     renter = Renter.objects.get(id=user.id)
    #     renter_id = renter.id
    # except Renter.DoesNotExist:
    #     messages.error(request, "You must be a registered renter to rent a room.")
    #     return HttpResponseRedirect(reverse("renthub:payment"))
    #
    # if Rental.objects.filter(room=room_id, renter=renter_id).exists():
    #     messages.info(request, "You have already rented this room.")

    return render(request, "renthub/payment.html", {"room": room})
