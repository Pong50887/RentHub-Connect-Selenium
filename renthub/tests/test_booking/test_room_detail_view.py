"""Tests of booking: DetailView changes related to booking feature."""
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter
from datetime import date


class RoomDetailViewTests(TestCase):
    """Tests of DetailView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter1 = Renter.objects.create_user(
            username='renter1', password='testpassword', phone_number='1234567890'
        )
        self.renter2 = Renter.objects.create_user(
            username='renter2', password='testpassword', phone_number='1234567890'
        )
        self.room = Room.objects.create(
            room_number=101, detail='A cozy room', price=1000.00
        )

    def test_non_existent_room(self):
        """Accessing a non-existent room redirects renter to the home page."""
        response = self.client.get(reverse('renthub:room', kwargs={'room_number': 999}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('renthub:home'))

    def test_renter_can_rent_available_room(self):
        """A renter can access an available room."""
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:room', kwargs={'room_number': self.room.room_number}),
                                   follow=True)
        self.assertContains(response, "Rent")

    def test_renter_cannot_rent_room_occupied_by_another_renter_message(self):
        """Another renter cannot rent a room associated with an existing rental within the same time range."""
        Rental.objects.create(
            renter=self.renter1,
            room=self.room,
            price=self.room.price,
            start_date=date.today(),
            end_date=date.today() + relativedelta(months=1)
        )

        self.client.login(username='renter2', password='testpassword')

        response = self.client.get(reverse('renthub:room', kwargs={'room_number': self.room.room_number}), follow=True)
        self.assertRedirects(response, reverse('renthub:home'))
        self.assertContains(response, "The room is not available.")

    def test_renter_can_rent_room_if_previous_rental_has_ended(self):
        """A renter can rent a room if the previous rental has ended."""
        past_end_date = date.today().replace(month=date.today().month - 1)
        Rental.objects.create(
            renter=self.renter1,
            room=self.room,
            price=self.room.price,
            start_date=past_end_date.replace(day=1),
            end_date=past_end_date,
        )

        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:room', kwargs={'room_number': self.room.room_number}), follow=True)
        self.assertContains(response, "Rent")
