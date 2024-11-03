from datetime import timedelta

from django.core.files.storage import default_storage
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from dateutil.relativedelta import relativedelta
from datetime import datetime

from ..models import Room, Renter, Rental, Transaction
from ..utils import generate_qr_code, delete_qr_code, get_rental_progress_data, Status


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
            Renter.objects.get(id=request.user.id)
        except Renter.DoesNotExist:
            messages.warning(request, "You need to register as a renter to proceed with a rental.")
            return redirect('renthub:rental', room_number=room.room_number)

        start_date = self.request.GET.get('rental_month')
        number_of_months = self.request.GET.get('number_of_months', 1)
        try:
            number_of_months = int(number_of_months)
        except ValueError:
            number_of_months = 1

        if start_date:
            if not room.is_available(start_date, number_of_months):
                messages.warning(request, "The room is not available for the selected rental period.")
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

            start_date_str = self.request.POST.get('start_date')
            number_of_months = self.request.POST.get('number_of_months', 1)
            try:
                number_of_months = int(number_of_months)
            except ValueError:
                number_of_months = 1

            start_date = datetime.strptime(start_date_str, "%Y-%m").replace(hour=7, minute=0, second=0)
            end_date = start_date + relativedelta(months=number_of_months)
            end_date = end_date + relativedelta(day=1) - timezone.timedelta(days=1)
            end_date = end_date.replace(hour=7, minute=0, second=0)

            rental, created = Rental.objects.get_or_create(
                room=room, renter=renter, defaults={'price': room.price*number_of_months,
                                                    'start_date': start_date,
                                                    'end_date': end_date,
                                                    }
            )
            rental.image = file_path
            rental.save()

            transaction, created = Transaction.objects.get_or_create(
                room=room, renter=renter, defaults={'date': datetime.now(), 'price': room.price}
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

        try:
            renter = Renter.objects.get(id=self.request.user.id)
            rental = Rental.objects.filter(renter=renter, room=room, start_date__lt=timezone.now() + timedelta(days=30),
                                           end_date__gt=timezone.now()).order_by('-id').first()
            if rental:
                context['rental'] = rental
                context['milestones'] = get_rental_progress_data(rental.status)

        except Renter.DoesNotExist:
            renter = None

        start_date = self.request.GET.get('rental_month')
        context['start_date'] = start_date

        number_of_months = self.request.GET.get('number_of_months', 1)
        try:
            number_of_months = int(number_of_months)
        except ValueError:
            number_of_months = 1
        context['number_of_months'] = number_of_months
        context['total_payment'] = room.price * number_of_months

        if not Rental.objects.filter(room=room, renter=renter).exclude(status=Status.reject).exists():
            generate_qr_code(room.price * number_of_months, room.room_number)
            context['qr_code_path'] = f"{settings.MEDIA_URL}qr_code_images/{room.room_number}.png"
            context['send_or_cancel'] = True
        else:
            context['qr_code_path'] = None
            context['send_or_cancel'] = False

        return context
