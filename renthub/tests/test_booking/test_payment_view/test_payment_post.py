"""Tests of booking: post method of PaymentView."""

from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter
import unittest


class PaymentViewPostTests(TestCase):
    """Tests of PaymentView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter1 = Renter.objects.create_user(username='renter1', password='testpassword',
                                                  phone_number='1234567890')
        self.renter2 = Renter.objects.create_user(username='renter2', password='testpassword',
                                                  phone_number='1234567890')
        self.room = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00)

        self.rental = Rental.objects.create(room=self.room, renter=self.renter1, price=self.room.price)

    @unittest.skip
    def test_rental_created_after_payment_submission(self):
        """A rental is created after a successful payment submission."""
        self.client.force_login(self.renter1)
        self.assertEqual(Rental.objects.count(), 0)
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'room_number': 'room_number'})
        self.assertEqual(Rental.objects.count(), 1)
        rental = Rental.objects.first()
        self.assertEqual(rental.renter, self.renter1)
        self.assertEqual(rental.room, self.room)

        self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_rental_not_created_if_payment_fails(self):
        """A rental is not created after a failed payment submission."""
        self.client.force_login(self.renter1)
        self.assertEqual(Rental.objects.count(), 0)
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.id}), {
            'room_number': 'room.id'})
        self.assertEqual(Rental.objects.count(), 0)
        self.assertEqual(response.status_code, 302)

    @unittest.skip
    def test_no_duplicate_rental(self):
        """A rental is not created if the same rental already exists."""
        self.client.force_login(self.renter1)
        self.assertEqual(Rental.objects.count(), 0)
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'room_number': 'room_number'})

        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'room_number': 'room_number'})

        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You already rented this room")
