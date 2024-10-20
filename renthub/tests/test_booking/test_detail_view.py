"""Tests of booking: DetailView changes related to booking feature."""

from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter


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

