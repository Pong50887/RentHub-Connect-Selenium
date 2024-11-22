from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from ....models import Rental, Room, Renter


class PaymentViewPostTests(TestCase):
    """Tests for RoomPaymentView's POST method."""

    def setUp(self):
        """Set up test data, including a room, and renters"""
        self.renter1 = Renter.objects.create_user(
            username='renter1',
            password='test_password',
            phone_number='1234567890'
        )
        self.renter2 = Renter.objects.create_user(
            username='renter2',
            password='test_password',
            phone_number='0987654321'
        )
        self.room = Room.objects.create(
            room_number=101,
            detail='A cozy room',
            price=1000.00
        )

    def test_rental_created_with_valid_payment_slip(self):
        """A rental is created after a valid payment slip submission."""
        self.client.force_login(self.renter1)
        payment_slip = SimpleUploadedFile("slip.png", b"dummy_image_data", content_type="image/png")
        self.assertEqual(Rental.objects.count(), 0)
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'payment_slip': payment_slip
        })
        self.assertEqual(Rental.objects.count(), 1)
        rental = Rental.objects.first()
        self.assertEqual(rental.renter, self.renter1)
        self.assertEqual(rental.room, self.room)
        self.assertEqual(rental.price, self.room.price)
        self.assertEqual(response.status_code, 302)

    def test_rental_not_created_if_no_payment_slip(self):
        """A rental is not created if no payment slip is provided."""
        self.client.force_login(self.renter1)
        self.assertEqual(Rental.objects.count(), 0)
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}))
        self.assertEqual(Rental.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No payment slip uploaded.")

    def test_no_duplicate_rental_creation(self):
        """Ensure no duplicate rental is created if one already exists."""
        self.client.force_login(self.renter1)
        payment_slip = SimpleUploadedFile("slip.png", b"dummy_image_data", content_type="image/png")
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'payment_slip': payment_slip
        })
        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'payment_slip': payment_slip
        })
        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('renthub:home'))

    def test_rental_status_update_on_resubmission(self):
        """Ensure an existing rental's status is updated if re-uploading a slip."""
        self.client.force_login(self.renter1)
        payment_slip = SimpleUploadedFile("slip.png", b"dummy_image_data", content_type="image/png")
        self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'payment_slip': payment_slip
        })
        rental = Rental.objects.first()
        self.assertEqual(rental.status, 'wait')
        payment_slip_new = SimpleUploadedFile("slip_new.png", b"dummy_image_data", content_type="image/png")
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'payment_slip': payment_slip_new
        })
        rental.refresh_from_db()
        self.assertEqual(rental.status, 'wait')
        self.assertEqual(response.status_code, 302)
