from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from mysite import settings

from ..models import Room, Rental, Renter
from ..utils import delete_qr_code


@login_required
def submit_payment(request, room_number):
    """Handle the submission of a rental payment.

    :param request: The HTTP request object.
    :param room_number: The room number for which the payment is being submitted.

    :return: Redirects to the rental page or renders the payment template
                       based on the rental status.
    """
    user = request.user
    if not user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    try:
        renter = Renter.objects.get(id=user.id)
    except Renter.DoesNotExist:
        messages.error(request, "You must be a registered renter to rent a room.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room_number}))

    try:
        room = Room.objects.get(room_number=room_number)
    except Room.DoesNotExist:
        messages.error(request, f"Room {room_number} does not exist.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room_number}))

    if Rental.objects.filter(room=room).exclude(renter=renter).exists():
        messages.error(request, "This room is already taken.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room.room_number}))

    rental_exists = Rental.objects.filter(room=room, renter=renter).exists()
    if rental_exists:
        messages.info(request, "You already rented this room")
        return render(request, "renthub/payment.html", {"room": room, "rental_exists": rental_exists})
    rental_fee = room.price * 1
    rental = Rental(room=room, renter=renter, rental_fee=rental_fee)
    rental.save()
    room.availability = False
    messages.info(request, "Your renting was successful")
    # Delete the QR code
    delete_qr_code(room_number)
    rental_exists = Rental.objects.filter(room=room, renter=renter).exists()
    return render(request, "renthub/payment.html", {"room": room, "rental_exists": rental_exists})
