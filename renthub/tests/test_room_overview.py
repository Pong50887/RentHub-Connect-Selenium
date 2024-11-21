from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Room, Rental, Renter
from ..utils import Status


class RoomOverviewViewTest(TestCase):
    """
    Tests for the Room Overview page to ensure proper functionality and access control.
    """

    def setUp(self):
        """Set up test data, including a superuser, a regular user, and test rooms and rentals."""
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin_password"
        )
        self.client.login(username="admin", password="admin_password")

        self.renter = Renter.objects.create(
            username="test_user",
            email="testuser@example.com",
            phone_number="1234567890",
            thai_citizenship_id="1234567890123"
        )

        self.room1 = Room.objects.create(room_number=101, detail='Test Room 1', price=1000.0)
        self.room2 = Room.objects.create(room_number=102, detail='Test Room 2', price=1200.0)

        Rental.objects.create(
            room=self.room2,
            renter=self.renter,
            status=Status.approve,
            is_paid=False,
            price=self.room2.price
        )

    def test_superuser_access(self):
        """Ensure that superusers can access the Room Overview page."""
        response = self.client.get(reverse('renthub:room_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'renthub/room_overview.html')

    def test_non_superuser_redirect(self):
        """Ensure that non-superusers are redirected to the home page with an error message."""
        self.client.logout()
        response = self.client.get(reverse('renthub:room_overview'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('renthub:home'))

        User.objects.create_user(
            username="regular_user",
            email="regularuser@example.com",
            password="password123"
        )
        self.client.login(username="regular_user", password="password123")
        response = self.client.get(reverse('renthub:room_overview'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('renthub:home'))

    def test_room_availability_context(self):
        """Verify that the Room Overview page provides correct context data for room availability."""
        response = self.client.get(reverse('renthub:room_overview'))
        rooms = response.context['rooms']

        room1_data = next(room for room in rooms if room['room_number'] == 101)
        room2_data = next(room for room in rooms if room['room_number'] == 102)

        self.assertTrue(room1_data['is_available'])
        self.assertIsNone(room1_data['renter_name'])
        self.assertIsNone(room1_data['is_paid'])

        self.assertFalse(room2_data['is_available'])
        self.assertEqual(room2_data['renter_name'], self.renter.username)
        self.assertFalse(room2_data['is_paid'])
