from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Room, Rental, Renter
from django.contrib import messages

def home(request):
    rooms = Room.objects.filter(availability=True)
    return render(request, "renthub/home.html", {"rooms": rooms})


def room(request, room_id):
    room = Room.objects.get(id=room_id)
    if room.availability == False:
        return HttpResponseRedirect(reverse("renthub:home"))
    return render(request, "renthub/rental.html", {"room": room})


def room_payment(request, room_id):
    room = Room.objects.get(id=room_id)
    user = request.user
    if room.availability == False:
        messages.error(request, f"The room {room} is currently unavailable.")
        return HttpResponseRedirect(reverse("renthub:home"))

    return render(request, "renthub/payment.html", {"room": room})

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
