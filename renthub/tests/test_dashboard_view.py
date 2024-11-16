from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from ...models import Room, Transaction, Renter


class DashboardViewTest(TestCase):
    """
    Test case for the dashboard view, which displays information about rooms and income.
    Includes tests for viewing the dashboard with or without selecting a specific month.
    """
    def setUp(self):
        """
        Set up the test data by creating rooms, renters, and transactions.
        """
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
            date=timezone.datetime(2023, 5, 1),
        )
        self.transaction_2 = Transaction.objects.create(
            renter=renter,
            room=self.room_2,
            price=Decimal('1200.00'),
            date=timezone.datetime(2023, 5, 10),
        )
        self.transaction_3 = Transaction.objects.create(
            renter=renter,
            room=self.room_1,
            price=Decimal('1000.00'),
            date=timezone.datetime(2023, 6, 1),
        )

    def test_dashboard_view_without_month(self):
        """
        Test the dashboard view when no month is specified, using the default for the selected year.
        Ensures the correct total income for the year and monthly income data.
        """
        response = self.client.get(reverse('renthub:dashboard') + '?year=2023')

        self.assertEqual(response.status_code, 200)
        self.assertIn('years', response.context)
        self.assertIn(2023, response.context['years'])
        self.assertIn('monthly_income_data', response.context)
        self.assertEqual(len(response.context['monthly_income_data']), 12)
        self.assertEqual(sum(response.context['monthly_income_data']), 3200.00)

    def test_dashboard_view_with_selected_month(self):
        """
        Test the dashboard view when a specific month is selected.
        Ensures the correct daily income data for the selected month.
        """
        response = self.client.get(reverse('renthub:dashboard') + '?year=2023&month=5')

        self.assertEqual(response.status_code, 200)
        self.assertIn('daily_income_data', response.context)
        self.assertEqual(len(response.context['daily_income_data']), 31)
        self.assertEqual(response.context['daily_income_data'][0], 1000.00)
        self.assertEqual(response.context['daily_income_data'][9], 1200.00)

    def test_no_transactions_for_selected_month(self):
        """
        Test the dashboard view when no transactions exist for the selected month.
        Verifies that the daily income data for that month is all zero.
        """
        response = self.client.get(reverse('renthub:dashboard') + '?year=2023&month=7')

        self.assertEqual(response.status_code, 200)
        self.assertIn('daily_income_data', response.context)
        self.assertEqual(len(response.context['daily_income_data']), 31)
        self.assertEqual(sum(response.context['daily_income_data']), 0)
