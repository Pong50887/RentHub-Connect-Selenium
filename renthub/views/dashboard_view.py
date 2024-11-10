from django.views.generic import ListView
from django.db.models import Sum
from ..models import Room, Transaction
from datetime import datetime


class DashboardView(ListView):
    """
    A view that displays the dashboard with information about rooms and income.
    """
    model = Room
    template_name = "renthub/dashboard.html"
    context_object_name = 'rooms'

    def get_context_data(self, **kwargs):
        """Override the get_context_data method to add custom context for the dashboard."""
        context = super().get_context_data(**kwargs)

        total_income = Transaction.objects.aggregate(total=Sum('price'))['total'] or 0

        current_month = datetime.now().month
        monthly_transactions = Transaction.objects.filter(date__month=current_month)
        monthly_income = monthly_transactions.aggregate(total=Sum('price'))['total'] or 0
        rooms_with_payments = monthly_transactions.values('room').distinct().count()

        total_rooms = Room.objects.count()

        income_percentage = (rooms_with_payments / total_rooms * 100) if total_rooms > 0 else 0

        context['total_income'] = total_income
        context['monthly_income'] = monthly_income
        context['income_percentage'] = income_percentage

        return context
