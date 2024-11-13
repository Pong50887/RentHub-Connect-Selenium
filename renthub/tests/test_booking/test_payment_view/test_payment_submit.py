from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages import get_messages
from renthub.models import Room, Rental, Renter
import os


class PaymentSubmitTest(TestCase):
    def setUp(self):
        # Create a test room and renter
        self.room = Room.objects.create(room_number=101, detail="Test Room", price=500)
        self.renter = Renter.objects.create_user(username="testuser", password="testpass")

        # Log in as the test renter
        self.client.login(username="testuser", password="testpass")

    def test_payment_submit_no_payment_slip(self):
        # Prepare form data without 'payment_slip'
        start_date = (timezone.now().replace(day=1)).strftime("%Y-%m")
        form_data = {
            'start_date': start_date,
            'number_of_months': 1
        }

        # Make the POST request
        url = reverse('renthub:payment', args=[self.room.room_number])
        response = self.client.post(url, form_data, follow=True)

        # Verify the page reloads with error message due to missing payment slip
        self.assertEqual(response.status_code, 200)  # No redirect on error
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("No payment slip uploaded." in str(m) for m in messages))

    def test_payment_submit_with_payment_slip(self):
        # Prepare form data with 'payment_slip' (simulated file upload)
        start_date = (timezone.now().replace(day=1)).strftime("%Y-%m")
        with open('test_payment_slip.png', 'wb') as f:
            f.write(b'fake image data')  # Simulate a payment slip file

        # Open the file for upload and simulate file upload
        with open('test_payment_slip.png', 'rb') as payment_slip:
            form_data = {
                'start_date': start_date,
                'number_of_months': 1,
                'payment_slip': payment_slip
            }

            # Make the POST request
            url = reverse('renthub:payment', args=[self.room.room_number])
            response = self.client.post(url, form_data, follow=True)

            # Verify the rental and transaction have been created
            rental = Rental.objects.filter(room=self.room, renter=self.renter).first()
            self.assertIsNotNone(rental)
            self.assertEqual(rental.room, self.room)
            self.assertEqual(rental.renter, self.renter)
            self.assertEqual(rental.price, self.room.price)

            # Verify the page reloads with success message
            self.assertEqual(response.status_code, 200)
            messages = list(get_messages(response.wsgi_request))
            self.assertTrue(any("Your rental request was submitted successfully!" in str(m) for m in messages))

        # Clean up the file after closing it
        os.remove('test_payment_slip.png')

    def test_start_date_before_end_date(self):
        # Define valid start and end dates where the start date is before the end date
        start_date = timezone.now()
        end_date = start_date + timedelta(days=30)

        # Create the rental instance
        rental = Rental.objects.create(
            room=self.room,
            renter=self.renter,
            start_date=start_date,
            end_date=end_date,
            price=self.room.price
        )

        # Test that the rental object is valid and saved correctly
        self.assertTrue(rental.start_date < rental.end_date)

    def test_rental_check_monthly_payment_due(self):
        today = timezone.now().date()
        start_date = today - timedelta(days=31)

        # Create the rental instance
        rental = Rental.objects.create(
            room=self.room,
            renter=self.renter,
            start_date=start_date,
            price=self.room.price
        )

        self.assertTrue(rental.is_paid)
        # Simulate the process where a rental is updated with a payment due
        rental.check_monthly_payment_due()

        # Check if the payment status is correctly marked as 'not paid'
        self.assertFalse(rental.is_paid)
