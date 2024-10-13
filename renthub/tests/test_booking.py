"""Tests of booking"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from renthub.models import Rental, Room, Renter


class RentalModelTests(TestCase):
    """Tests of Rental object creation"""

    def setUp(self):
        """Set up data for the tests."""
        self.renter = Renter.objects.create(username="normal_user", password="test123", phone_number="1234567890")
        self.admin = User.objects.create_superuser(username='admin', password='adminpassword',
                                                   email='admin@example.com')
        self.room = Room.objects.create(room_number="101", detail='A cozy room', price=1000.00, availability=True)

    def test_renter_can_create_rental(self):
        """A renter can create a rental."""
        rental = Rental.objects.create(room=self.room, renter=self.renter, rental_fee=self.room.price)
        self.assertIsInstance(rental, Rental)
        self.assertEqual(rental.renter, self.renter)

    def test_non_renter_cannot_create_rental(self):
        """A non-renter cannot create a rental."""
        with self.assertRaises(Exception):
            Rental.objects.create(room=self.room, renter=self.admin, rental_fee=self.room.price)


class DetailViewTests(TestCase):
    """Tests of DetailView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter1 = Renter.objects.create_user(username='renter1', password='testpassword',
                                                  phone_number='1234567890')
        self.renter2 = Renter.objects.create_user(username='renter2', password='testpassword',
                                                  phone_number='1234567890')
        self.room = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00, availability=False)

    def test_occupied_room_message(self):
        """Another renter cannot rent a room associated with an existing rental belonging to another
        renter. """
        Rental.objects.create(renter=self.renter1, room=self.room, rental_fee=self.room.price)

        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:rental', kwargs={'room_number': self.room.room_number}), follow=True)
        self.assertContains(response, "This room is taken.")


class PaymentViewTests(TestCase):
    """Tests of PaymentView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter1 = Renter.objects.create_user(username='renter1', password='testpassword', phone_number='1234567890')
        self.renter2 = Renter.objects.create_user(username='renter2', password='testpassword', phone_number='1234567890')
        self.room = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00, availability=True)
        self.rental = Rental.objects.create(room=self.room, renter=self.renter1, rental_fee=self.room.price)

    def test_payment_access_for_authenticated_renter(self):
        """An authenticated renter can access the payment page."""
        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(f'/renthub/rental/{self.room.room_number}/payment/')
        self.assertEqual(response.status_code, 200)

    def test_payment_access_for_unauthenticated_user(self):
        """An unauthenticated user cannot access the payment page."""
        response = self.client.get(f'/renthub/rental/{self.room.room_number}/payment/')
        self.assertEqual(response.status_code, 302)  # Redirected

    def test_payment_access_for_non_owner_renter(self):
        """A renter who tried to view a payment page of a room associated with a rental belonging to another renter
        is redirected to rental page. """
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:payment', kwargs={'room_number': self.room.room_number}))

        self.assertEqual(response.status_code, 302)  # Redirect to rental page
        self.assertRedirects(response, reverse('renthub:rental', kwargs={'room_number': self.room.room_number}))


class PaymentListViewTests(TestCase):
    """Tests of PaymentListView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter1 = Renter.objects.create_user(username='renter1', password='testpassword', phone_number='1234567890')
        self.renter2 = Renter.objects.create_user(username='renter2', password='testpassword', phone_number='1234567890')
        self.room1 = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00, availability=True)
        self.room2 = Room.objects.create(room_number=102, detail='A cozy room', price=1000.00, availability=True)
        Rental.objects.create(room=self.room1, renter=self.renter1, rental_fee=self.room1.price)
        Rental.objects.create(room=self.room2, renter=self.renter1, rental_fee=self.room2.price)

    def test_no_rental_message_for_renter_without_rentals(self):
        """A renter without any rental sees that their payment list page is empty."""
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:payment_list'))
        self.assertContains(response, "You currently have no payments")

    def test_rental_display_for_renter_with_rentals(self):
        """A renter with any rental sees all of their existing rental in their payment list page."""
        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:payment_list'))
        self.assertContains(response, "Room Number: 101")
        self.assertContains(response, "Room Number: 102")


class PaymentSubmitTests(TestCase):
    """Tests of payment submission method"""

    def setUp(self):
        """Set up data for the tests."""
        self.renter = Renter.objects.create(username='regular_user', password='password', phone_number='1234567890')
        self.room = Room.objects.create(room_number='101', price=5000, availability=True)

    def test_rental_created_after_payment_submission(self):
        """A rental is created after a successful payment submission."""
        self.client.force_login(self.renter)
        self.assertEqual(Rental.objects.count(), 0)
        response = self.client.post(reverse('renthub:submit', kwargs={'room_number': self.room.room_number}), {
            'room_number': 'room_number'})
        self.assertEqual(Rental.objects.count(), 1)
        rental = Rental.objects.first()
        self.assertEqual(rental.renter, self.renter)
        self.assertEqual(rental.room, self.room)

        self.assertEqual(response.status_code, 200)

    def test_rental_not_created_if_payment_fails(self):
        """A rental is not created after a failed payment submission."""
        self.client.force_login(self.renter)
        self.assertEqual(Rental.objects.count(), 0)
        response = self.client.post(reverse('renthub:submit', kwargs={'room_number': self.room.id}), {
            'room_number': 'room.id'})
        self.assertEqual(Rental.objects.count(), 0)
        self.assertEqual(response.status_code, 302)

    def test_no_duplicate_rental(self):
        """A rental is not created if the same rental already exists."""
        self.client.force_login(self.renter)
        self.assertEqual(Rental.objects.count(), 0)
        response = self.client.post(reverse('renthub:submit', kwargs={'room_number': self.room.room_number}), {
            'room_number': 'room_number'})

        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('renthub:submit', kwargs={'room_number': self.room.room_number}), {
            'room_number': 'room_number'})

        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You already rented this room")


class PaymentCancelTests(TestCase):
    """Tests of payment cancellation method."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter = Renter.objects.create(username="normal_user", password="test123", phone_number="1234567890")
        self.renter1 = Renter.objects.create(username="normal_user1", password="test123", phone_number="1234567890")
        self.renter2 = Renter.objects.create(username="normal_user2", password="test123", phone_number="1234567890")
        self.room = Room.objects.create(room_number="101", detail='A cozy room', price=1000.00, availability=True)

    def test_renter_can_cancel_rental(self):
        """A renter can cancel their own rental."""
        self.client.force_login(self.renter)
        rental = Rental.objects.create(room=self.room, renter=self.renter, rental_fee=self.room.price)
        response = self.client.post(reverse('renthub:cancel', args=[self.room.room_number]))
        self.assertFalse(Rental.objects.filter(id=rental.id).exists())
        self.room.refresh_from_db()
        self.assertTrue(self.room.availability)
        self.assertContains(response, "Your booking cancellation was successful.")

    def test_renter_cannot_cancel_other_renters_rental(self):
        """A renter cannot cancel another renter's rental."""
        self.client.force_login(self.renter1)
        rental = Rental.objects.create(room=self.room, renter=self.renter1, rental_fee=self.room.price)
        self.client.force_login(self.renter2)
        response = self.client.post(reverse('renthub:cancel', kwargs={'room_number': self.room.room_number}))
        self.assertTrue(Rental.objects.filter(id=rental.id).exists())
        self.assertContains(response, "You do not have an active booking for this room.")
