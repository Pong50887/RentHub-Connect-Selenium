from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

from mysite import settings
from ..models import Room, Rental, Renter


@login_required
def cancel_rental(request, room_number):
    """
    Handle the cancellation of a rental for the specified room.

    :param request: The HTTP request object.
    :param room_number: The number of the room to cancel the rental for.

    :return: Redirects to the rental page for the room.
    """
    room = Room.objects.get(room_number=room_number)
    user = request.user
    if not user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    try:
        renter = Renter.objects.get(id=user.id)
    except Renter.DoesNotExist:
        messages.error(request, "You must be a registered renter to cancel a rental.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room_number}))

    try:
        rental = Rental.objects.get(room=room, renter=renter)
        rental.delete()
        room.availability = True
        room.save()
        messages.info(request, "Your booking cancellation was successful.")
    except Rental.DoesNotExist:
        messages.warning(request, "You do not have an active booking for this room.")

    return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room_number}))
