from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
from ..models import Room, Transaction, Renter


class DashboardViewTest(TestCase):
    """
    Tests for the Dashboard view, focusing on income data summaries and filtering by year and month.
    """

    def setUp(self):
        """Set up test data for dashboard testing, including users, rooms, and transactions."""
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password123'
        )
        self.client.login(username='admin', password='password123')

        self.room_1 = Room.objects.create(
            room_number=101,
            room_floor=1,
            detail="Room with a view",
            price=Decimal('1000.00'),
        )
        self.room_2 = Room.objects.create(
            room_number=102,
            room_floor=1,
            detail="Cozy room",
            price=Decimal('1200.00'),
        )

        renter = Renter.objects.create(username="John Doe")

        self.transaction_1 = Transaction.objects.create(
            renter=renter,
            room=self.room_1,
            price=Decimal('1000.00'),
            date=timezone.make_aware(timezone.datetime(2023, 5, 1)),
        )
        self.transaction_2 = Transaction.objects.create(
            renter=renter,
            room=self.room_2,
            price=Decimal('1200.00'),
            date=timezone.make_aware(timezone.datetime(2023, 5, 10)),
        )
        self.transaction_3 = Transaction.objects.create(
            renter=renter,
            room=self.room_1,
            price=Decimal('1000.00'),
            date=timezone.make_aware(timezone.datetime(2023, 6, 1)),
        )

    def test_dashboard_view_without_month(self):
        """Test the dashboard view's response and data for a selected year without specifying a month."""
        response = self.client.get(reverse('renthub:dashboard') + '?year=2023')
        self.assertEqual(response.status_code, 200)
        self.assertIn('years', response.context)
        self.assertIn(2023, response.context['years'])
        self.assertIn('monthly_income_data', response.context)
        self.assertEqual(len(response.context['monthly_income_data']), 12)
        self.assertEqual(sum(response.context['monthly_income_data']), 3200.00)

    def test_dashboard_view_with_selected_month(self):
        """Test the dashboard view's response and data for a selected year and month."""
        response = self.client.get(reverse('renthub:dashboard') + '?year=2023&month=5')
        self.assertEqual(response.status_code, 200)
        self.assertIn('daily_income_data', response.context)
        self.assertEqual(len(response.context['daily_income_data']), 31)
        self.assertEqual(response.context['daily_income_data'][0], 1000.00)
        self.assertEqual(response.context['daily_income_data'][9], 1200.00)

    def test_no_transactions_for_selected_month(self):
        """Test the dashboard view's response when there are no transactions for the selected month."""
        response = self.client.get(reverse('renthub:dashboard') + '?year=2023&month=7')
        self.assertEqual(response.status_code, 200)
        self.assertIn('daily_income_data', response.context)
        self.assertEqual(len(response.context['daily_income_data']), 31)
        self.assertEqual(sum(response.context['daily_income_data']), 0)
