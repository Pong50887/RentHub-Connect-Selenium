from datetime import timedelta

from django.core.files.storage import default_storage
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Room, Renter, Rental
from ..utils import generate_qr_code, get_rental_progress_data, Status


class RoomPaymentView(LoginRequiredMixin, DetailView):
    """
    View for displaying the payment page for a specific room rental.
    """
    model = Room
    template_name = "renthub/payment.html"
    context_object_name = "room"

    def get_object(self, queryset=None):
        """Retrieve the room object based on the room number provided in the URL."""
        room_number = self.kwargs.get("room_number")
        room = get_object_or_404(Room, room_number=room_number)
        return room

    def get(self, request, *args, **kwargs):
        """Handle GET requests to display the room payment page."""
        room = self.get_object()

        try:
            renter = Renter.objects.get(id=request.user.id)
        except Renter.DoesNotExist:
            messages.warning(request, "You need to register as a renter to proceed with a rental.")
            return redirect('renthub:rental', room_number=room.room_number)

        if Rental.objects.filter(room=room).exclude(renter=renter).exclude(status=Status.reject).exists():
            messages.warning(request, "Someone else already rented this room.")
            return redirect('renthub:rental', room_number=room.room_number)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle POST requests to upload a payment slip."""
        room = self.get_object()

        try:
            renter = Renter.objects.get(id=request.user.id)
        except Renter.DoesNotExist:
            messages.error(request, "You need to register as a renter before submitting a payment.")
            return self.get(request, *args, **kwargs)

        if 'payment_slip' in request.FILES:
            payment_slip = request.FILES['payment_slip']

            file_path = default_storage.save(f'slip_images/{room.room_number}_{renter.id}.png', payment_slip)

            rental, created = Rental.objects.get_or_create(
                room=room, renter=renter, defaults={'price': room.price}
            )
            rental.image = file_path
            rental.save()

            messages.success(request, "Payment slip uploaded successfully!")
            return redirect('renthub:home')
        else:
            messages.error(request, "No payment slip uploaded.")

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add additional context data to the template."""
        context = super().get_context_data(**kwargs)
        room = self.get_object()

        try:
            renter = Renter.objects.get(id=self.request.user.id)
            rental = Rental.objects.filter(renter=renter, room=room, start_date__lt=timezone.now() + timedelta(days=30),
                                           end_date__gt=timezone.now()).order_by('-id').first()
            if rental:
                context['rental'] = rental
                context['milestones'] = get_rental_progress_data(rental.status)

        except Renter.DoesNotExist:
            renter = None

        generate_qr_code(room.price, room.room_number)

        context['qr_code_path'] = f"media/qr_code_images/{room.room_number}.png"
        context['send_or_cancel'] = True

        if Rental.objects.filter(room=context['room'], renter=renter).exclude(status=Status.reject).exists():
            context['send_or_cancel'] = False

        return context
