"""
Tests of booking: PaymentView changes related to booking feature.
    Changes included in this module: Payment View QR code accessibility.
"""
from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter
from renthub.utils import Status
from django.utils import timezone
from datetime import datetime


class PaymentViewTests(TestCase):
    """Tests of PaymentView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter = Renter.objects.create_user(username='renter1', password='testpassword',
                                                 phone_number='1234567890')
        self.room1 = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00)
        self.room2 = Room.objects.create(room_number=102, detail='A cozy room', price=1000.00)
        self.start_date = timezone.make_aware(datetime(2024, 1, 1))
        self.end_date = timezone.make_aware(datetime(2025, 1, 1))

    def test_qr_base_case(self):
        """A renter can see the QR code if they don't have a Rental for the room."""
        self.client.login(username='renter1', password='testpassword')

        start_date_str = '2024-01'
        end_date_str = '2024-12'
        url = reverse('renthub:payment', kwargs={'room_number': self.room2.room_number})
        url_with_params = f"{url}?start_month={start_date_str}&end_month={end_date_str}"

        response = self.client.get(url_with_params)
        self.assertContains(response, 'Scan this QR code to complete the payment')

    def test_qr_not_visible_if_rental_exists(self):
        """A renter cannot see the QR code if they already have a Rental for the room."""
        Rental.objects.create(room=self.room1, renter=self.renter, price=self.room1.price)
        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room1.room_number}))
        self.assertNotContains(response, 'Scan this QR code to complete the payment')

    def test_qr_visible_if_latest_rental_is_rejected(self):
        """A renter cannot see the QR code if they have a Rental for the room and their latest RentalRequest
        has been rejected. """
        Rental.objects.create(room=self.room2, renter=self.renter, price=1200.00, status=Status.reject)
        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room2.room_number}))
        self.assertContains(response, 'Scan this QR code to complete the payment')
