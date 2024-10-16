from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Room, Rental, Renter
from ..utils import generate_qr_code


class RoomPaymentView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = "renthub/payment.html"
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
            messages.error(request, f"The room {room} is currently unavailable.")
            return HttpResponseRedirect(reverse("renthub:home"))

        try:
            renter = Renter.objects.get(id=request.user.id)
        except Renter.DoesNotExist:
            renter = None
            messages.warning(request, "You need to register as a renter to proceed with a rental.")

        if Rental.objects.filter(room=room).exclude(renter=renter).exists():
            messages.error(request, "This room is already taken.")
            return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room.room_number}))

        rental_exists = Rental.objects.filter(room=room, renter=renter).exists()
        if rental_exists:
            messages.info(request, "You already have a rental for this room.")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()

        try:
            renter = Renter.objects.get(id=self.request.user.id)
        except Renter.DoesNotExist:
            renter = None

        generate_qr_code(room.price, room.room_number)

        context['qr_code_path'] = f"media/qr_code_images/{room.room_number}.png"
        context['rental_exists'] = Rental.objects.filter(room=context['room'], renter=renter).exists()

        return context
