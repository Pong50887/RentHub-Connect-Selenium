"""Tests of booking: PaymentHistoryView changes related to booking feature."""

from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter

# almost identical to payment_list, but only RentalRequests here
# have trailing status info
