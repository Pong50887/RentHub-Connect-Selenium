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


class PaymentStatusBaseTests(TestCase):
    """Base test class for PaymentStatus tests."""

    def setUp(self):
        """Set up data for PaymentStatus tests."""
        self.renter = Renter.objects.create_user(
            username='renter',
            password='testpassword',
            phone_number='1234567890'
        )
        self.room = Room.objects.create(
            room_number=101,
            detail='A cozy room',
            price=1000.00
        )
        self.client.login(username='renter', password='testpassword')

        # Prepare payment slip
        self.payment_slip_filename = 'test_payment_slip.png'
        payment_slip_data = b'fake image data'
        self.payment_slip = SimpleUploadedFile(
            name=self.payment_slip_filename,
            content=payment_slip_data,
            content_type='image/png'
        )

        # Submit form to create rental and transaction
        self.create_rental()

    def create_rental(self):
        """Helper to create a rental with initial data."""
        start_date = timezone.now().replace(day=1).strftime("%Y-%m")
        form_data = {
            'start_date': start_date,
            'number_of_months': 1,
            'payment_slip': self.payment_slip,
            'total': str(self.room.price),  # Set the price for the transaction
        }

        url = reverse('renthub:payment', args=[self.room.room_number])
        self.client.post(url, form_data, follow=True)

    def update_rental_status(self, status):
        """Helper to update the rental status."""
        admin = RentalAdmin(Rental, site)
        rental = Rental.objects.get(renter=self.renter, room=self.room)
        rental.status = status
        admin.save_model(None, rental, None, change=True)
        rental.refresh_from_db()
        return rental

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.payment_slip_filename):
            os.remove(self.payment_slip_filename)


class PaymentStatusWaitTests(TestCase):
    """Tests of PaymentStatus when status is wait."""

    def setUp(self):
        """Set up data for the PaymentStatusWaitTests."""
        self.renter = Renter.objects.create_user(
            username='renter',
            password='testpassword',
            phone_number='1234567890'
        )
        self.room = Room.objects.create(
            room_number=101,
            detail='A cozy room',
            price=1000.00
        )
        self.client.login(username='renter', password='testpassword')

        self.payment_slip_filename = 'test_payment_slip.png'
        payment_slip_data = b'fake image data'
        payment_slip = SimpleUploadedFile(
            name=self.payment_slip_filename,
            content=payment_slip_data,
            content_type='image/png'
        )
        start_date = timezone.now().replace(day=1).strftime("%Y-%m")

        # Include 'total' in the form data to prevent the error
        form_data = {
            'start_date': start_date,
            'number_of_months': 1,
            'payment_slip': payment_slip,
            'total': '1000.00'  # Set the total price for the transaction
        }

        url = reverse('renthub:payment', args=[self.room.room_number])
        self.client.post(url, form_data, follow=True)

        admin = RentalAdmin(Rental, site)

        # Retrieve the created rental and set its status to 'wait'
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
        transaction = Transaction.objects.filter(room=self.room).first()
        self.assertIsNotNone(transaction, "Transaction should exist after payment submission.")

        response = self.client.get(reverse('renthub:payment_history', kwargs={'pk': transaction.id}))
        content = response.content.decode('utf-8')
        self.assertIn(str(Status.wait).title(), content, f"'{str(Status.wait).title()}' not found in response.")


class PaymentStatusApproveTests(PaymentStatusBaseTests):
    """Tests of PaymentStatus when status is approved."""

    def setUp(self):
        """Set up data for the PaymentStatusApproveTests."""
        super().setUp()
        self.update_rental_status(Status.approve)

    def test_payment_list_view(self):
        """A renter can see their ongoing rentals and transaction with approve status."""
        response = self.client.get(reverse('renthub:payment_list'))
        content = response.content.decode('utf-8')

        self.assertIn(str(Status.approve), content, f"Status '{Status.approve}' should appear in the response.")

        rental_history_pos = content.find('Rental History')
        first_approve_pos = content.find(str(Status.approve))
        second_approve_pos = content.find(str(Status.approve), rental_history_pos)

        self.assertLess(
            first_approve_pos, rental_history_pos,
            f"'{Status.approve}' does not appear after 'Ongoing Rentals'"
        )
        self.assertGreater(
            second_approve_pos, rental_history_pos,
            f"'{Status.approve}' does not appear after 'Rental History'."
        )

    def test_payment_view(self):
        """A renter can see their payment status on the payment page updated to approved."""
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}))
        content = response.content.decode('utf-8')
        self.assertIn('Approved', content, "'Approved' not found in response.")

    def test_payment_history_view(self):
        """A renter can see their payment history with approve status."""
        # Ensure the transaction is created and retrieve its ID
        transaction = Transaction.objects.filter(room=self.room).first()
        self.assertIsNotNone(transaction, "Transaction should exist after payment submission.")

        response = self.client.get(reverse('renthub:payment_history', kwargs={'pk': transaction.id}))
        content = response.content.decode('utf-8')
        self.assertIn(str(Status.approve).title(), content, f"'{str(Status.approve).title()}' not found in response.")


class PaymentStatusRejectTests(PaymentStatusBaseTests):
    """Tests of PaymentStatus when status is reject."""

    def setUp(self):
        """Set up data for the PaymentStatusRejectTests."""
        super().setUp()
        self.update_rental_status(Status.reject)

    def test_payment_list_view(self):
        """Rentals with reject status should not show up on ongoing rentals list, but should appear in transactions."""
        response = self.client.get(reverse('renthub:payment_list'))
        content = response.content.decode('utf-8')

        self.assertIn(str(Status.reject), content, f"Status '{Status.reject}' should appear in the response.")

        rental_history_pos = content.find('Rental History')
        first_reject_pos = content.find(str(Status.reject))

        self.assertGreater(
            first_reject_pos, rental_history_pos,
            f"'{Status.reject}' does not appear after 'Rental History'."
        )

    def test_payment_history_view(self):
        """A renter can see their payment history with reject status."""
        # Ensure the transaction is created and retrieve its ID
        transaction = Transaction.objects.filter(room=self.room).first()
        self.assertIsNotNone(transaction, "Transaction should exist after payment submission.")

        response = self.client.get(reverse('renthub:payment_history', kwargs={'pk': transaction.id}))
        content = response.content.decode('utf-8')
        self.assertIn(str(Status.reject).title(), content,
                      f"'{str(Status.reject).title()}' not found in response.")
