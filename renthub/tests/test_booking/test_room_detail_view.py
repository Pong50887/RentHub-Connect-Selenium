"""Tests of booking: DetailView changes related to booking feature."""

from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter
from renthub.utils import Status
import unittest


class RoomDetailViewTests(TestCase):
    """Tests of DetailView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter1 = Renter.objects.create_user(username='renter1', password='testpassword',
                                                  phone_number='1234567890')
        self.renter2 = Renter.objects.create_user(username='renter2', password='testpassword',
                                                  phone_number='1234567890')
        self.room = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00)

    def test_non_existent_room(self):
        """Accessing a non-existent room redirects renter to home page."""
        response = self.client.get(reverse('renthub:room', kwargs={'room_number': 999}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('renthub:home'))

    def test_renter_can_rent_available_room(self):
        """A renter can access an available room."""
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:room', kwargs={'room_number': self.room.room_number}),
                                   follow=True)
        self.assertContains(response, "Rent")

    @unittest.skip("1. cannot rent the same room within the same time period. "
                   "2. can rent the same room with non-overlapping time period.")
    def test_renter_cannot_rent_room_occupied_by_another_renter_message(self):
        """Another renter cannot rent a room associated with an existing rental belonging to another
        renter within the same time range."""
        # before admin approve feature
        Rental.objects.create(renter=self.renter1, room=self.room, price=self.room.price)
        self.room.save()

        self.client.login(username='renter2', password='testpassword')

        response = self.client.get(reverse('renthub:room', kwargs={'room_number': self.room.room_number}), follow=True)
        self.assertContains(response, "This room is already taken.")

    def test_renter_cannot_rent_room_they_have_already_rented_message(self):
        """Another renter cannot rent a room associated with an existing rental belonging to another renter. """
        Rental.objects.create(renter=self.renter1, room=self.room, price=self.room.price, status=Status.approve)

        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:room', kwargs={'room_number': self.room.room_number}), follow=True)
        self.assertContains(response, "You have rented this room.")

    def test_renter_already_submitted_a_rent(self):
        """Accessing a room in which the renter have already submitted a rental payment of this room"""
        Rental.objects.create(renter=self.renter1, room=self.room, price=self.room.price)

        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:room', kwargs={'room_number': self.room.room_number}), follow=True)
        self.assertContains(response, "Please wait for admin to review your rental request.")
