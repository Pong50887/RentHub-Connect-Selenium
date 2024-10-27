"""Tests of booking: payment status."""

from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter


class PaymentStatusTests(TestCase):
    """Tests of PaymentStatus."""

    def setUp(self):
        """Set up data for the tests."""

# ** change according to actions
# submited
# admin approved
# admin disapproved

# status in payment_list view
# status in payment view

# status in payment history view
