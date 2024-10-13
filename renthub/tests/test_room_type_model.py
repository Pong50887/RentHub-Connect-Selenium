from django.test import TestCase
from renthub.models import RoomType


class RoomTypeModelTest(TestCase):
    def setUp(self):
        """Set up data for the tests."""
        self.room_type = RoomType.objects.create(type_name="Single Bed",
                                                 description="Room with a bed",
                                                 ideal_for="One person")

    def test_room_type_creation(self):
        """Test that the RoomType instance can be created successfully."""
        self.assertEqual(self.room_type.type_name, "Single Bed")
        self.assertEqual(self.room_type.description, 'Room with a bed')
        self.assertEqual(self.room_type.ideal_for, "One person")

    def test_string_representation(self):
        """Test the string representation of the RoomType model."""
        self.assertEqual(str(self.room_type), 'Single Bed')
