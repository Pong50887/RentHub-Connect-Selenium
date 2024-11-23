import calendar
from datetime import datetime
from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Sum

from ..models import Room, Transaction


class DashboardView(ListView):
    """
    A view that displays the dashboard with information about rooms and income.
    """
    model = Room
    template_name = "renthub/dashboard.html"
    context_object_name = 'rooms'

    def dispatch(self, request, *args, **kwargs):
        """
        Restrict access to superusers only.
        """
        if not request.user.is_superuser:
            messages.error(request, "You do not have permission to access the dashboard.")
            return redirect('renthub:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Override the get_context_data method to add custom context for the dashboard."""
        context = super().get_context_data(**kwargs)

        try:
            year = int(self.request.GET.get('year', datetime.now().year))
        except ValueError:
            year = datetime.now().year

        try:
            month = int(self.request.GET.get('month', 0))
        except ValueError:
            month = 0

        years = Transaction.objects.values('date__year').distinct().order_by('date__year')
        context['years'] = [y['date__year'] for y in years]

        context['months'] = [(i, calendar.month_name[i]) for i in range(1, 13)]

        transaction_filter = {'date__year': year}
        if month:
            transaction_filter['date__month'] = month

        filtered_transactions = Transaction.objects.filter(**transaction_filter)
        total_income = filtered_transactions.aggregate(total=Sum('price'))['total'] or 0

        monthly_income_data = []
        for m in range(1, 13):
            income = Transaction.objects.filter(date__month=m,
                                                date__year=year).aggregate(total=Sum('price'))['total'] or 0
            monthly_income_data.append(float(income))

        daily_income_data = []
        if month:
            days_in_month = calendar.monthrange(year, month)[1]
            for d in range(1, days_in_month + 1):
                income = Transaction.objects.filter(
                    date__year=year, date__month=month, date__day=d
                ).aggregate(total=Sum('price'))['total'] or 0
                daily_income_data.append(float(income))

        context['total_income'] = total_income
        context['monthly_income_data'] = monthly_income_data
        context['daily_income_data'] = daily_income_data
        context['selected_year'] = year
        context['selected_month'] = month
        context['selected_month_name'] = calendar.month_name[month] if month else None

        return context
