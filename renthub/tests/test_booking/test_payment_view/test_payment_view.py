"""
Tests of booking: PaymentView changes related to booking feature.
    Changes included in this module: Payment View accessibility depending on users.
"""

from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter, RentalRequest


class PaymentViewTests(TestCase):
    """Tests of PaymentView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter1 = Renter.objects.create_user(username='renter1', password='testpassword',
                                                  phone_number='1234567890')
        self.renter2 = Renter.objects.create_user(username='renter2', password='testpassword',
                                                  phone_number='1234567890')
        self.room = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00, availability=True)

        self.rental = Rental.objects.create(room=self.room, renter=self.renter1, rental_fee=self.room.price)

    def test_payment_access_for_authenticated_renter(self):
        """An authenticated renter can access the payment page."""
        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}))
        self.assertEqual(response.status_code, 200)

    def test_payment_access_for_unauthenticated_user(self):
        """An unauthenticated user cannot access the payment page."""
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}))
        self.assertEqual(response.status_code, 302)

    def test_payment_access_for_non_owner_renter(self):
        """A renter who tried to view a payment page of a room associated with a rental belonging to another renter
        is redirected to rental page. """
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('renthub:rental', kwargs={'room_number': self.room.room_number}))
