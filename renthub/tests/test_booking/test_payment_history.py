"""Tests of booking: PaymentHistoryView changes related to booking feature."""

from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter

# almost identical to payment_list, but only Transactions here
# have trailing status info (My Rentals)

# and Payment history details page
