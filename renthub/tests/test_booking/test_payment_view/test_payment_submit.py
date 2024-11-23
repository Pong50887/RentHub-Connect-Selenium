from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages import get_messages
from renthub.models import Room, Rental, Renter, Transaction
import os


class PaymentSubmitTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(room_number=101, detail="Test Room", price=500)
        self.renter = Renter.objects.create_user(username="testuser", password="testpass")

        self.client.login(username="testuser", password="testpass")

    def test_payment_submit_no_payment_slip(self):
        start_date = (timezone.now().replace(day=1)).strftime("%Y-%m")
        form_data = {
            'start_date': start_date,
            'number_of_months': 1
        }

        url = reverse('renthub:payment', args=[self.room.room_number])
        response = self.client.post(url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("No payment slip uploaded." in str(m) for m in messages))

    def test_payment_submit_with_payment_slip(self):
        """Test submitting a payment slip successfully."""
        start_date = timezone.now().replace(day=1).strftime("%Y-%m")

        # Create a dummy payment slip file
        with open('test_payment_slip.png', 'wb') as f:
            f.write(b'fake image data')

        with open('test_payment_slip.png', 'rb') as payment_slip:
            # Prepare the form data with price information
            form_data = {
                'start_date': start_date,
                'number_of_months': 1,
                'payment_slip': payment_slip,
                'total': '1000.00'  # Ensure the price is included
            }

            url = reverse('renthub:payment', args=[self.room.room_number])
            response = self.client.post(url, form_data, follow=True)

            # Ensure a rental has been created for the room and renter
            rental = Rental.objects.filter(room=self.room, renter=self.renter).first()
            self.assertIsNotNone(rental)
            self.assertEqual(rental.room, self.room)
            self.assertEqual(rental.renter, self.renter)
            self.assertEqual(rental.price, self.room.price)

            # Ensure the transaction was created
            transaction = Transaction.objects.filter(room=self.room, renter=self.renter).first()
            self.assertIsNotNone(transaction)
            self.assertEqual(transaction.price, 1000.00)  # Ensure the transaction has the correct price

            # Ensure the response is successful
            self.assertEqual(response.status_code, 200)

            # Check for success message
            messages = list(get_messages(response.wsgi_request))
            self.assertTrue(any("Your rental request was submitted successfully!" in str(m) for m in messages))

        # Clean up the test file
        os.remove('test_payment_slip.png')

    def test_start_date_before_end_date(self):
        start_date = timezone.now()
        end_date = start_date + timedelta(days=30)

        rental = Rental.objects.create(
            room=self.room,
            renter=self.renter,
            start_date=start_date,
            end_date=end_date,
            price=self.room.price
        )

        self.assertTrue(rental.start_date < rental.end_date)

    def test_rental_check_monthly_payment_due(self):
        today = timezone.now().date()
        start_date = today - timedelta(days=31)

        rental = Rental.objects.create(
            room=self.room,
            renter=self.renter,
            start_date=start_date,
            price=self.room.price
        )

        self.assertTrue(rental.is_paid)
        rental.check_monthly_payment_due()

        self.assertFalse(rental.is_paid)
