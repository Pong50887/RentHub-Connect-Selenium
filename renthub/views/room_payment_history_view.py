from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Transaction


class RoomPaymentHistoryView(LoginRequiredMixin, ListView):
    """
    View to list rooms associated with the logged-in renter's rentals.
    """
    model = Transaction
    template_name = "renthub/payment_history.html"
    context_object_name = "transactions"

    def get_queryset(self):
        """Return a queryset of rooms linked to the logged-in user's rentals."""
        transactions = Transaction.objects.filter(renter__id=self.request.user.id)

        return transactions
