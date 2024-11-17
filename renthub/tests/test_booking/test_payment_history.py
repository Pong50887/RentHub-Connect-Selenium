"""Tests of booking: PaymentHistoryView changes related to booking feature."""
import os

from django.contrib.admin import site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from renthub.admin import RentalAdmin
from renthub.models import Rental, Room, Renter, Transaction
from renthub.utils import Status


class PaymentListViewTests(TestCase):
    """Tests of payment history in PaymentListView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter = Renter.objects.create_user(username='renter', password='testpassword',
                                                 phone_number='1234567890')
        self.room = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00)
        self.client.login(username='renter', password='testpassword')

        self.payment_slip_filename = 'test_payment_slip.png'
        payment_slip_data = b'fake image data'
        payment_slip = SimpleUploadedFile(
            name=self.payment_slip_filename,
            content=payment_slip_data,
            content_type='image/png'
        )
        start_date = (timezone.now().replace(day=1)).strftime("%Y-%m")
        self.form_data = {
            'start_date': start_date,
            'number_of_months': 1,
            'payment_slip': payment_slip
        }
        self.admin = RentalAdmin(Rental, site)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.payment_slip_filename):
            os.remove(self.payment_slip_filename)

    def test_no_rental_history(self):
        """Have no initial rental history."""
        response = self.client.get(reverse('renthub:payment_list'))
        content = response.content.decode('utf-8')
        self.assertIn('You currently have no rental history.', content)

    def test_have_rental_history(self):
        """Have rental history after submitted a rental payment slip."""
        url = reverse('renthub:payment', args=[self.room.room_number])
        self.client.post(url, self.form_data, follow=True)

        response = self.client.get(reverse('renthub:payment_list'))
        content = response.content.decode('utf-8')
        rental_history_pos = content.find('Rental History')
        transaction_pos = content.find(f'{self.room.room_number}', rental_history_pos)
        self.assertGreater(
            transaction_pos, rental_history_pos,
            f"'{self.room.room_number}' does not appear after 'Rental History'."
        )

    def test_have_rental_history_after_rental_rejected(self):
        """Still have rental history after rental was rejected."""
        url = reverse('renthub:payment', args=[self.room.room_number])
        self.client.post(url, self.form_data, follow=True)
        rental = Rental.objects.get(renter=self.renter, room=self.room)
        rental.status = Status.reject
        self.admin.save_model(None, rental, None, change=True)
        rental.refresh_from_db()

        response = self.client.get(reverse('renthub:payment_list'))
        content = response.content.decode('utf-8')
        rental_history_pos = content.find('Rental History')
        transaction_pos = content.find(f'{self.room.room_number}', rental_history_pos)
        self.assertGreater(
            transaction_pos, rental_history_pos,
            f"'{self.room.room_number}' does not appear after 'Rental History'."
        )


class PaymentHistoryViewTests(TestCase):
    """Tests of PaymentHistoryView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter = Renter.objects.create_user(username='renter', password='testpassword',
                                                 phone_number='1234567890')
        self.room = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00)
        self.client.login(username='renter', password='testpassword')

        self.payment_slip_filename = 'test_payment_slip.png'
        payment_slip_data = b'fake image data'
        payment_slip = SimpleUploadedFile(
            name=self.payment_slip_filename,
            content=payment_slip_data,
            content_type='image/png'
        )
        start_date = (timezone.now().replace(day=1)).strftime("%Y-%m")
        self.form_data = {
            'start_date': start_date,
            'number_of_months': 1,
            'payment_slip': payment_slip
        }
        self.admin = RentalAdmin(Rental, site)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.payment_slip_filename):
            os.remove(self.payment_slip_filename)

    def test_can_access_payment_history_page(self):
        """Can access payment history page after submitted a rental payment slip."""
        url = reverse('renthub:payment', args=[self.room.room_number])
        self.client.post(url, self.form_data, follow=True)

        response = self.client.get(reverse('renthub:payment_history',
                                           kwargs={'pk': Transaction.objects.get(room=self.room).id}))
        content = response.content.decode('utf-8')
        self.assertIn(f'{self.room.room_number}', content)
