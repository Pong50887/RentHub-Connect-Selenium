"""Tests of booking: PaymentListView changes related to booking feature."""

from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter


class PaymentListViewTests(TestCase):
    """Tests of PaymentListView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter1 = Renter.objects.create_user(username='renter1', password='testpassword', phone_number='1234567890')
        self.renter2 = Renter.objects.create_user(username='renter2', password='testpassword', phone_number='1234567890')
        self.room1 = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00)
        self.room2 = Room.objects.create(room_number=102, detail='A cozy room', price=1000.00)
        self.room3 = Room.objects.create(room_number=103, detail='A cozy room', price=1000.00)
        Rental.objects.create(room=self.room1, renter=self.renter1, price=self.room1.price)
        Rental.objects.create(room=self.room2, renter=self.renter1, price=self.room2.price)
        # RentalRequest.objects.create(room=self.room3, renter=self.renter1, price=self.room3.price)

    def test_no_rental_message_for_renter_without_rentals(self):
        """A renter without any rental sees that their payment list page is empty."""
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:payment_list'))
        self.assertContains(response, "You currently have no ongoing rentals.")

    def test_rental_display_for_renter_with_rentals(self):
        """A renter with any rental sees all of their existing rental(s) in their payment list page."""
        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:payment_list'))
        self.assertContains(response, "101")
        self.assertContains(response, "102")