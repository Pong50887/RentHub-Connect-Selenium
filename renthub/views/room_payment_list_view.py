from datetime import datetime, date
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Room, Rental, Transaction, Notification
from django.db.models import F
from ..utils import Status


class RoomPaymentListView(LoginRequiredMixin, TemplateView):
    """
    View to list rooms associated with the logged-in renter's rentals.
    """
    template_name = "renthub/payment_list.html"

    def get_context_data(self, **kwargs):
        """Return the context of data displayed on My Rentals page."""
        context = super().get_context_data(**kwargs)
        rentals = Rental.objects.filter(renter__id=self.request.user.id).exclude(status=Status.reject)

        if rentals:
            rooms_with_rentals = Room.objects.filter(
                rental__in=rentals
            ).annotate(
                status=F('rental__status'),
                is_paid=F('rental__is_paid')
            )

            context['rooms'] = rooms_with_rentals

            rental = rentals.first()
            today = date.today()
            rental_start_date = rental.start_date
            six_months_after_start = rental_start_date + relativedelta(months=5)
            if today.day <= 15:
                target_month = today + relativedelta(months=1)
            else:
                target_month = today + relativedelta(months=2)

            context['target_month'] = target_month.strftime('%Y-%m')
            context['in_month'] = target_month.strftime('%Y-%m') > six_months_after_start.strftime('%Y-%m')

            if rental:
                context['rental_start_date'] = rental.start_date
                context['rental_end_date'] = rental.end_date

        transactions = Transaction.objects.filter(renter__id=self.request.user.id).order_by('-date')
        context['transactions'] = transactions
        return context

    def post(self, request, *args, **kwargs):
        end_month_str = request.POST.get('end_month')
        end_month = datetime.strptime(end_month_str, "%Y-%m")
        new_end_date = end_month - relativedelta(days=1)
        end_month_last_day = new_end_date.date()
        admin = User.objects.get(username="rhadmin")
        rental = Rental.objects.filter(renter__id=self.request.user.id).exclude(status=Status.reject).first()
        rental.end_date = end_month_last_day
        rental.save()

        Notification.objects.create(
            renter=admin,
            title="Payment Due",
            message=f"{self.request.user.username} has selected {end_month_str} "
                    f"as their move-out month. Please review and prepare for their departure.",
            post_date=timezone.now(),
            is_read=False
        )
        messages.success(request, "Your Move-Out Notice has been sent successfully.")

        return redirect('renthub:payment_list')
