from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from mysite import settings

from ..models import Room, Rental, Renter
from ..utils import delete_qr_code, Status


@login_required
def submit_payment(request, room_number):
    """Handle the submission of a rental payment and create a RentalRequest.

    :param request: The HTTP request object.
    :param room_number: The room number for which the payment is being submitted.
    :return: Redirects to the rental page or renders the payment template.
    """
    user = request.user
    if not user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    try:
        renter = get_object_or_404(Renter, id=user.id)
    except Http404:
        messages.error(request, "This renter does not exist.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room_number}))

    try:
        room = get_object_or_404(Room, room_number=room_number)
    except Http404:
        messages.error(request, "This room does not exist.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room_number}))

    if Rental.objects.filter(room=room).exclude(renter=renter).exists():
        messages.error(request, "This room is already taken.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room_number}))

    rental_exists = Rental.objects.filter(room=room, renter=renter).exists()
    if rental_exists:
        messages.info(request, "You already rented this room.")
        return render(request, "renthub/payment.html", {"room": room, "rental_exists": rental_exists})

    rental = Rental.objects.filter(renter=renter, room=room).order_by('-id').first()
    if rental:
        if rental.status != Status.reject:
            messages.warning(request, "You cannot submit a new rental request until the previous one is rejected.")
            return render(request, "renthub/payment.html", {"room": room, "rental_exists": rental_exists})

    # Proceed with rental logic
    rental_fee = room.price * 1  # Adjust if needed
    Rental.objects.create(room=room, renter=renter, rental_fee=rental_fee)
    messages.success(request, f"Rental for room {room_number} submitted successfully.")

    room.availability = False
    room.save()

    # Delete the QR code
    delete_qr_code(room_number)

    rental_exists = Rental.objects.filter(room=room, renter=renter).exists()
    return render(request, "renthub/payment.html", {"room": room, "rental_exists": rental_exists})
