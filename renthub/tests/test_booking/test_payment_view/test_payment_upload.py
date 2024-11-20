"""
Tests of booking: PaymentView changes related to booking feature.
    Changes included in this module: Payment View photo uploading feature accessibility.
"""
from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter
from renthub.utils import Status


class PaymentViewTests(TestCase):
    """Tests of PaymentView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter = Renter.objects.create_user(username='renter1', password='testpassword',
                                                 phone_number='1234567890')
        self.room1 = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00)
        self.room2 = Room.objects.create(room_number=102, detail='A cozy room', price=1000.00)

    def test_photo_upload_base_case(self):
        """A renter can upload a payment photo if they don't have an active Rental for the room."""
        self.client.login(username='renter1', password='testpassword')

        start_date_str = '2024-01'
        end_date_str = '2024-12'
        url = reverse('renthub:payment', kwargs={'room_number': self.room2.room_number})
        url_with_params = f"{url}?start_month={start_date_str}&end_month={end_date_str}"

        response = self.client.get(url_with_params)
        self.assertContains(response, 'Upload Payment Slip:')

    def test_photo_upload_not_visible_if_rental_exists(self):
        """A renter cannot upload a payment photo if they already have an active Rental for the room."""
        Rental.objects.create(room=self.room1, renter=self.renter, price=self.room1.price)
        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room1.room_number}))
        self.assertRedirects(response, reverse('renthub:home'))

    def test_photo_upload_visible_if_rental_is_rejected(self):
        """A renter can upload a payment photo if their latest RentalRequest for the room was rejected."""
        Rental.objects.create(room=self.room2, renter=self.renter, price=1200.00, status=Status.reject)
        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room2.room_number}))
        self.assertContains(response, 'Upload Payment Slip:')
