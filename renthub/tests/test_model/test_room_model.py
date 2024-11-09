from django.test import TestCase
from renthub.models import RoomType, Room


class RoomModelTest(TestCase):
    def setUp(self):
        """Set up data for the tests."""
        self.room_type = RoomType.objects.create(type_name="Single Bed",
                                                 description="Room with a bed",
                                                 ideal_for="One person")
        self.room = Room.objects.create(room_number=101,
                                        detail='Test Room',
                                        price=99.99,
                                        room_type=self.room_type)

    def test_room_creation(self):
        """Test that the Room instance can be created successfully."""
        self.assertEqual(self.room.room_number, 101)
        self.assertEqual(self.room.detail, 'Test Room')
        self.assertEqual(self.room.price, 99.99)
        self.assertEqual(self.room.room_type, self.room_type)

    # def test_room_availability(self):
    #     """Test room availability filter."""
    #     available_rooms = Room.objects.filter(availability=True)
    #     self.assertIn(self.room, available_rooms)

    def test_string_representation(self):
        """Test the string representation of the Room model."""
        self.assertEqual(str(self.room), 'Room 101 - Test Room')
