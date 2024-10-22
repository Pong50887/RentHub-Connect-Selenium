"""
Tests of booking: PaymentView changes related to booking feature.
    Changes included in this module: Payment View send/cancel button changes.
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
        self.room1 = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00, availability=True)
        self.room2 = Room.objects.create(room_number=102, detail='A cozy room', price=1000.00, availability=True)

        self.rental = Rental.objects.create(room=self.room1, renter=self.renter1, rental_fee=self.room1.price)

    def test_cancel_button_visible_if_rental_exist(self):
        """The cancel button is visible if the renter has an active rental for the room."""
        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room1.room_number}))
        self.assertContains(response, 'Cancel Renting')

    def test_cancel_button_not_visible_if_no_rental(self):
        """The cancel button is not visible if the renter has no active rental for the room."""
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room2.room_number}))
        self.assertNotContains(response, 'Cancel Renting')

    def test_cancel_button_visible_if_rental_request_status_is_wait(self):
        """The cancel button visibility in case rental request status is 'wait'."""
        RentalRequest.objects.create(room=self.room2, renter=self.renter2, price=1200.00)
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room2.room_number}))
        self.assertContains(response, 'Please wait for admin to review your rental request.')

    def test_cancel_button_visible_if_rental_request_is_approved(self):
        """The cancel button visibility in case rental request status is 'approve'."""
        RentalRequest.objects.create(room=self.room2, renter=self.renter2, price=1200.00, status='approve')
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room2.room_number}))
        self.assertContains(response, 'Cancel Renting')

    def test_cancel_button_not_visible_if_rental_request_is_rejected(self):
        """The cancel button visibility in case rental request status is 'reject'."""
        RentalRequest.objects.create(room=self.room2, renter=self.renter2, price=1200.00, status='reject')
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room2.room_number}))
        self.assertNotContains(response, 'Cancel Renting')
