"""Tests of booking: DetailView changes related to booking feature."""

from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter, RentalRequest
from renthub.utils import Status


class DetailViewTests(TestCase):
    """Tests of DetailView."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter1 = Renter.objects.create_user(username='renter1', password='testpassword',
                                                  phone_number='1234567890')
        self.renter2 = Renter.objects.create_user(username='renter2', password='testpassword',
                                                  phone_number='1234567890')
        self.room = Room.objects.create(room_number=101, detail='A cozy room', price=1000.00, availability=True)

    def test_non_existent_room(self):
        """Accessing a non-existent room redirects renter to home page."""
        response = self.client.get(reverse('renthub:rental', kwargs={'room_number': 999}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('renthub:home'))

    def test_renter_can_rent_available_room(self):
        """A renter can access an available room."""
        self.client.login(username='renter2', password='testpassword')
        response = self.client.get(reverse('renthub:rental', kwargs={'room_number': self.room.room_number}),
                                   follow=True)
        self.assertContains(response, "Rent")

    def test_renter_cannot_rent_room_occupied_by_another_renter_message(self):
        """Another renter cannot rent a room associated with an existing rental belonging to another
        renter. """
        # before admin approve feature
        Rental.objects.create(renter=self.renter1, room=self.room, rental_fee=self.room.price)
        self.room.availability = False
        self.room.save()

        self.client.login(username='renter2', password='testpassword')

        response = self.client.get(reverse('renthub:rental', kwargs={'room_number': self.room.room_number}), follow=True)
        self.assertContains(response, "This room is already taken.")

    def test_renter_cannot_rent_room_they_have_already_rented_message(self):
        """Another renter cannot rent a room associated with an existing rental belonging to another renter. """
        # before admin approve feature
        Rental.objects.create(renter=self.renter1, room=self.room, rental_fee=self.room.price)
        self.room.availability = False
        self.room.save()

        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:rental', kwargs={'room_number': self.room.room_number}), follow=True)
        self.assertContains(response, "This room is already taken.")

    def test_renter_already_submitted_a_rent_request(self):
        """Accessing a room in which the renter have already submitted a RentalRequest of this room but is not yet
        approved nor rejected. """
        # before submit function is fixed
        RentalRequest.objects.create(renter=self.renter1, room=self.room, price=self.room.price)

        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:rental', kwargs={'room_number': self.room.room_number}), follow=True)
        self.assertContains(response, "This room is already taken.")

    def test_renter_latest_rent_request_was_rejected(self):
        """Accessing a room in which the renter whose RentalRequest of this room is rejected is allowed to rent
        again."""
        # before submit function is fixed
        RentalRequest.objects.create(renter=self.renter1, room=self.room, price=self.room.price, status=Status.reject.value)

        self.client.login(username='renter1', password='testpassword')
        response = self.client.get(reverse('renthub:rental', kwargs={'room_number': self.room.room_number}), follow=True)

        self.assertEqual(response.status_code, 200)

        rent_url = reverse('renthub:payment', kwargs={'room_number': self.room.room_number})
        self.assertContains(response, f'<a href="{rent_url}" class="btn btn-success">Rent</a>', html=True)

