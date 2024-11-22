from django.core.files.storage import default_storage
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from datetime import datetime, date

from renthub.models import Room, Renter, Rental, Transaction, RentalPayment
from renthub.utils import generate_qr_code, delete_qr_code, get_rental_progress_data, Status, get_room_images


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
        """
        Handle GET requests with a validation check.
        Redirect to the home page if the user is not eligible to access this page.
        """
        room = self.get_object()

        try:
            renter = Renter.objects.get(id=request.user.id)
        except Renter.DoesNotExist:
            messages.error(request, "You need to register as a renter to view this page.")
            return redirect('renthub:home')

        if not room.is_available() and not Rental.objects.filter(room=room, renter=renter).exists():
            messages.error(request, "This room is not available.")
            return redirect('renthub:home')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle POST requests to upload a payment slip."""
        room = self.get_object()
        total = (request.POST.get('total'))
        if total:
            float(total)

        try:
            renter = Renter.objects.get(id=request.user.id)
        except Renter.DoesNotExist:
            messages.error(request, "You need to register as a renter before submitting a payment.")
            return self.get(request, *args, **kwargs)

        if 'payment_slip' in request.FILES:
            payment_slip = request.FILES['payment_slip']

            file_path = default_storage.save(f'slip_images/{room.room_number}_{renter.id}.png', payment_slip)

            rental = Rental.objects.filter(room=room, renter=renter).exclude(status=Status.reject).first()

            if not rental:
                now = timezone.now()

                if now.month == 12:
                    start_date = timezone.datetime(now.year + 1, 1, 1)
                else:
                    start_date = timezone.datetime(now.year, now.month + 1, 1)

                rental, created = Rental.objects.get_or_create(
                    room=room, renter=renter, defaults={'price': room.price,
                                                        'start_date': start_date,
                                                        'last_checked_month': start_date,
                                                        'last_paid_date': start_date,
                                                        }
                )
                rental.image = file_path
                rental.save()

                transaction = Transaction.objects.create(
                    room=room,
                    renter=renter,
                    price=room.price,
                    date=datetime.now(),
                    image=file_path
                )
                transaction.image = file_path
                transaction.save()
                messages.success(request, "Your rental request was submitted successfully!")
                delete_qr_code(room.room_number)

            else:
                rental.status = Status.wait
                rental.save()
                rental_payment = RentalPayment.objects.create(
                    room=room,
                    renter=renter,
                    price=total,
                    image=file_path,
                    status=Status.wait,
                )
                rental_payment.save()

                transaction = Transaction.objects.create(
                    room=room,
                    renter=renter,
                    price=room.price,
                    date=datetime.now(),
                    image=file_path
                )
                transaction.image = file_path
                transaction.save()
                messages.success(request, "Your rental request was submitted successfully!")
                delete_qr_code(room.room_number)
            return redirect('renthub:home')
        else:
            messages.error(request, "No payment slip uploaded.")

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add additional context data to the template."""
        context = super().get_context_data(**kwargs)
        room = self.get_object()

        if room.room_type:
            context["room_images"] = get_room_images(room.room_type)

        try:
            renter = Renter.objects.get(id=self.request.user.id)
            rental = Rental.objects.filter(renter=renter, room=room).order_by('-id').first()
            if rental:
                context['milestones'] = get_rental_progress_data(rental.status)

        except Renter.DoesNotExist:
            renter = None

        rental = Rental.objects.filter(room=room, renter=renter).exclude(status=Status.reject).first()
        context['rental'] = rental
        context['deposit'] = room.price * 2

        today = date.today()
        if today.day > 15:
            days_late = today.day - 15
            additional_charge = days_late * 50
        else:
            additional_charge = 0

        if rental:
            context['total'] = room.price + rental.water_fee + rental.electric_fee + additional_charge
            context['additional_charge'] = additional_charge
            context['water'] = rental.water_fee
            context['electric'] = rental.electric_fee
        else:
            context['total'] = room.price * 3

        if not rental:
            generate_qr_code(room.price * 3, room.room_number)
            context['qr_code_path'] = f"{settings.MEDIA_URL}qr_code_images/{room.room_number}.png"
            context['send_or_cancel'] = True
            context['qr_code_owner_name'] = "Achirawich"
        else:
            if not rental.is_paid:
                generate_qr_code(room.price + rental.water_fee + rental.electric_fee + additional_charge,
                                 room.room_number)
                context['qr_code_path'] = f"{settings.MEDIA_URL}qr_code_images/{room.room_number}.png"
                context['send_or_cancel'] = True
                context['qr_code_owner_name'] = "Achirawich"
            else:
                context['qr_code_path'] = None
                context['send_or_cancel'] = False
                context['qr_code_owner_name'] = "N/A"

        return context
