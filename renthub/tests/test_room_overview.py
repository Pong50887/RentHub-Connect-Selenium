from django.test import TestCase
from django.urls import reverse
from ..models import Room, Rental, Renter
from ..utils import Status


class RoomOverviewViewTest(TestCase):

    def setUp(self):
        # Create test renter
        self.renter = Renter.objects.create(
            username="testuser",
            email="testuser@example.com",
            phone_number="1234567890",
            thai_citizenship_id="1234567890123"
        )

        # Create rooms
        self.room1 = Room.objects.create(room_number=101, detail='Test Room', price=99.99,)
        self.room2 = Room.objects.create(room_number=102, detail='Test Room', price=99.99,)

        # Create rentals for the rooms (room2 will have an active rental)
        self.rental1 = Rental.objects.create(
            room=self.room2,
            renter=self.renter,
            status=Status.approve,
            is_paid=False,
            price=self.room1.price
        )

    def test_room_overview_view_success(self):
        """Test that the room overview page loads successfully and displays room information."""
        response = self.client.get(reverse('renthub:room_overview'))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'renthub/room_overview.html')

        # Check if rooms are in the context
        self.assertIn('rooms', response.context)

        # Check if room 1 is available and room 2 is occupied
        room1_data = next(room for room in response.context['rooms'] if room['room_number'] == 101)
        room2_data = next(room for room in response.context['rooms'] if room['room_number'] == 102)

        # Room 1 should be available
        self.assertTrue(room1_data['is_available'])
        self.assertIsNone(room1_data['renter_name'])
        self.assertIsNone(room1_data['is_paid'])

        # Room 2 should be occupied, unpaid, with renter details
        self.assertFalse(room2_data['is_available'])
        self.assertEqual(room2_data['renter_name'], 'testuser')
        self.assertFalse(room2_data['is_paid'])

    def test_no_rooms_available(self):
        """Test if no rooms are available."""
        # Set the rental status of all rooms to 'approve' (occupied)
        Rental.objects.create(
            room=self.room1,
            renter=self.renter,
            status=Status.approve,
            is_paid=False,
            price=self.room1.price
        )
        response = self.client.get(reverse('renthub:room_overview'))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure both rooms are occupied
        room1_data = next(room for room in response.context['rooms'] if room['room_number'] == 101)
        room2_data = next(room for room in response.context['rooms'] if room['room_number'] == 102)

        self.assertFalse(room1_data['is_available'])
        self.assertFalse(room2_data['is_available'])

    def test_room_with_no_active_rentals(self):
        """Test that rooms without any active rentals are marked as available."""
        # No rentals for room1 (it should be available)
        room1_data = next(room for room in self.client.get(reverse('renthub:room_overview')).context['rooms'] if
                          room['room_number'] == 101)
        self.assertTrue(room1_data['is_available'])
