from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from renthub.models import Rental, Room, Renter, Transaction


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

        # Set a total amount for the transaction (simulate form data)
        total = '1000.00'

        # Ensure the rental does not exist yet
        self.assertEqual(Rental.objects.count(), 0)

        # Post a valid payment slip to create rental and transaction
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'payment_slip': payment_slip,
            'total': total  # Simulate the total amount field
        })

        # Ensure that rental and transaction are created
        self.assertEqual(Rental.objects.count(), 1)
        rental = Rental.objects.first()

        # Check if the rental object has correct data
        self.assertEqual(rental.renter, self.renter1)
        self.assertEqual(rental.room, self.room)
        self.assertEqual(rental.price, self.room.price)

        # Ensure a Transaction was created with the correct price
        transaction = Transaction.objects.filter(room=self.room, renter=self.renter1).first()
        self.assertIsNotNone(transaction, "Transaction was not created.")
        self.assertEqual(transaction.price, float(total), "Transaction price does not match rental price.")

        self.assertEqual(response.status_code, 302)

    def test_rental_not_created_if_no_payment_slip(self):
        """A rental is not created if no payment slip is provided."""
        self.client.force_login(self.renter1)

        # Ensure no rentals exist before the test
        self.assertEqual(Rental.objects.count(), 0)

        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}))

        # Ensure no rental is created
        self.assertEqual(Rental.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No payment slip uploaded.")

    def test_no_duplicate_rental_creation(self):
        """Ensure no duplicate rental is created if one already exists."""
        self.client.force_login(self.renter1)
        payment_slip = SimpleUploadedFile("slip.png", b"dummy_image_data", content_type="image/png")

        # Post a valid payment slip to create rental
        total = '1000.00'  # Simulate the total amount
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'payment_slip': payment_slip,
            'total': total  # Include the total value
        })
        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

        # Try posting again with the same payment slip
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'payment_slip': payment_slip,
            'total': total  # Include the total value
        })

        # Ensure no duplicate rental was created
        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('renthub:home'))

    def test_rental_status_update_on_resubmission(self):
        """Ensure an existing rental's status is updated if re-uploading a slip."""
        self.client.force_login(self.renter1)
        payment_slip = SimpleUploadedFile("slip.png", b"dummy_image_data", content_type="image/png")

        # Submit the initial payment slip
        total = '1000.00'  # Simulate the total amount
        self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'payment_slip': payment_slip,
            'total': total  # Include the total value
        })

        # Get the rental and check its status
        rental = Rental.objects.first()
        self.assertEqual(rental.status, 'wait')

        # Submit a new payment slip to update the status
        payment_slip_new = SimpleUploadedFile("slip_new.png", b"dummy_image_data", content_type="image/png")
        response = self.client.post(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}), {
            'payment_slip': payment_slip_new,
            'total': total  # Include the total value
        })

        # Refresh and check if the status remains 'wait'
        rental.refresh_from_db()
        self.assertEqual(rental.status, 'wait')
        self.assertEqual(response.status_code, 302)
