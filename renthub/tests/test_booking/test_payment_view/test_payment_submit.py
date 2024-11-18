from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages import get_messages
from renthub.models import Room, Rental, Renter
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
        start_date = (timezone.now().replace(day=1)).strftime("%Y-%m")
        with open('test_payment_slip.png', 'wb') as f:
            f.write(b'fake image data')

        with open('test_payment_slip.png', 'rb') as payment_slip:
            form_data = {
                'start_date': start_date,
                'number_of_months': 1,
                'payment_slip': payment_slip
            }

            url = reverse('renthub:payment', args=[self.room.room_number])
            response = self.client.post(url, form_data, follow=True)

            rental = Rental.objects.filter(room=self.room, renter=self.renter).first()
            self.assertIsNotNone(rental)
            self.assertEqual(rental.room, self.room)
            self.assertEqual(rental.renter, self.renter)
            self.assertEqual(rental.price, self.room.price)

            self.assertEqual(response.status_code, 200)
            messages = list(get_messages(response.wsgi_request))
            self.assertTrue(any("Your rental request was submitted successfully!" in str(m) for m in messages))

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
