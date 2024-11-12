from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Room, Rental, Transaction
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

        rooms_with_rentals = Room.objects.filter(
            rental__in=rentals
        ).annotate(
            status=F('rental__status'),
            is_paid=F('rental__is_paid')
        )

        context['rooms'] = rooms_with_rentals

        transactions = Transaction.objects.filter(renter__id=self.request.user.id).order_by('-date')
        context['transactions'] = transactions
        return context
