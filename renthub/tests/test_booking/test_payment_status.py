"""Tests of booking: payment status."""
import os

from django.contrib.admin import site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from renthub.admin import RentalAdmin
from renthub.models import Rental, Room, Renter, Transaction
from renthub.utils import Status


class PaymentStatusWaitTests(TestCase):
    """Tests of PaymentStatus when status is wait."""

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
        form_data = {
            'start_date': start_date,
            'number_of_months': 1,
            'payment_slip': payment_slip
        }

        url = reverse('renthub:payment', args=[self.room.room_number])
        self.client.post(url, form_data, follow=True)

        admin = RentalAdmin(Rental, site)

        rental = Rental.objects.get(renter=self.renter, room=self.room)
        rental.status = Status.wait
        admin.save_model(None, rental, None, change=True)
        rental.refresh_from_db()

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.payment_slip_filename):
            os.remove(self.payment_slip_filename)

    def test_payment_list_view(self):
        """A renter can see their ongoing rentals and transaction with wait status."""
        response = self.client.get(reverse('renthub:payment_list'))

        content = response.content.decode('utf-8')

        self.assertIn(str(Status.wait), content, f"Status '{Status.wait}' should appear in the response.")

        rental_history_pos = content.find('Rental History')
        first_wait_pos = content.find(str(Status.wait))
        second_wait_pos = content.find(str(Status.wait), rental_history_pos)

        self.assertLess(
            first_wait_pos, rental_history_pos,
            f"'{Status.wait}' does not appear after 'Ongoing Rentals'"
        )
        self.assertGreater(
            second_wait_pos, rental_history_pos,
            f"'{Status.wait}' does not appear after 'Rental History'."
        )

    def test_payment_view(self):
        """A renter can see their payment status on payment page."""
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}))
        content = response.content.decode('utf-8')
        self.assertIn('Submitted', content, "'Submitted' not found in response.")
        self.assertIn('Pending', content, "'Pending' not found in response.")

    def test_payment_history_view(self):
        """A renter can see their payment history with wait status."""
        response = self.client.get(reverse('renthub:payment_history', kwargs={'pk': Transaction.objects.get(room=self.room).id}))
        content = response.content.decode('utf-8')
        self.assertIn(str(Status.wait).title(), content, f"'{str(Status.wait).title()}' not found in response.")


class PaymentStatusApproveTests(TestCase):
    """Tests of PaymentStatus when status is approve."""

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
        form_data = {
            'start_date': start_date,
            'number_of_months': 1,
            'payment_slip': payment_slip
        }

        url = reverse('renthub:payment', args=[self.room.room_number])
        self.client.post(url, form_data, follow=True)

        admin = RentalAdmin(Rental, site)

        rental = Rental.objects.get(renter=self.renter, room=self.room)
        rental.status = Status.approve
        admin.save_model(None, rental, None, change=True)
        rental.refresh_from_db()

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.payment_slip_filename):
            os.remove(self.payment_slip_filename)

    def test_payment_list_view(self):
        """A renter can see their ongoing rentals and transaction with approve status."""
        response = self.client.get(reverse('renthub:payment_list'))

        content = response.content.decode('utf-8')

        self.assertIn(str(Status.approve), content, f"Status '{Status.approve}' should appear in the response.")

        rental_history_pos = content.find('Rental History')
        first_wait_pos = content.find(str(Status.approve))
        second_wait_pos = content.find(str(Status.approve), rental_history_pos)

        self.assertLess(
            first_wait_pos, rental_history_pos,
            f"'{Status.approve}' does not appear after 'Ongoing Rentals'"
        )
        self.assertGreater(
            second_wait_pos, rental_history_pos,
            f"'{Status.approve}' does not appear after 'Rental History'."
        )

    def test_payment_view(self):
        """A renter can see their payment status on payment page has been updated."""
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}))
        content = response.content.decode('utf-8')
        self.assertIn('Approved', content, "'Approved' not found in response.")

    def test_payment_history_view(self):
        """A renter can see their payment history with approve status."""
        response = self.client.get(reverse('renthub:payment_history', kwargs={'pk': Transaction.objects.get(room=self.room).id}))
        content = response.content.decode('utf-8')
        self.assertIn(str(Status.approve).title(), content, f"'{str(Status.approve).title()}' not found in response.")


class PaymentStatusRejectTests(TestCase):
    """Tests of PaymentStatus when status is reject."""

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
        form_data = {
            'start_date': start_date,
            'number_of_months': 1,
            'payment_slip': payment_slip
        }

        url = reverse('renthub:payment', args=[self.room.room_number])
        self.client.post(url, form_data, follow=True)

        admin = RentalAdmin(Rental, site)

        rental = Rental.objects.get(renter=self.renter, room=self.room)
        rental.status = Status.reject
        admin.save_model(None, rental, None, change=True)
        rental.refresh_from_db()

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.payment_slip_filename):
            os.remove(self.payment_slip_filename)

    def test_payment_list_view(self):
        """A rentals with reject status should not show up on ongoing rentals list, but show up on transaction."""
        response = self.client.get(reverse('renthub:payment_list'))

        content = response.content.decode('utf-8')

        self.assertIn(str(Status.reject), content, f"Status '{Status.reject}' should appear in the response.")

        rental_history_pos = content.find('Rental History')
        first_wait_pos = content.find(str(Status.reject))

        self.assertGreater(
            first_wait_pos, rental_history_pos,
            f"'{Status.reject}' does not appear after 'Rental History'."
        )

    def test_payment_history_view(self):
        """A renter can see their payment history with wait status."""
        response = self.client.get(reverse('renthub:payment_history', kwargs={'pk': Transaction.objects.get(room=self.room).id}))
        content = response.content.decode('utf-8')
        self.assertIn(str(Status.reject).title(), content, f"'{str(Status.reject).title()}' not found in response.")
