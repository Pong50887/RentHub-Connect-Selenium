from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Transaction


class RoomPaymentHistoryView(LoginRequiredMixin, DetailView):
    """
    View to see the rental payments details.
    """
    model = Transaction
    template_name = "renthub/payment_history.html"
    context_object_name = "transaction"
