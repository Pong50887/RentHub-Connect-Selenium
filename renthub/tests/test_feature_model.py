from django.test import TestCase
from renthub.models import RoomType, Feature


class FeatureModelTest(TestCase):
    def setUp(self):
        """Set up data for the tests."""
        self.room_type = RoomType.objects.create(type_name="Single Bed",
                                                 description="Room with a bed",
                                                 ideal_for="One person")

        self.feature = Feature.objects.create(room_type=self.room_type,
                                              name="nothing")

    def test_feature_creation(self):
        """Test that the Feature instance can be created successfully."""
        self.assertEqual(str(self.feature.room_type), "Single Bed")
        self.assertEqual(self.feature.name, "nothing")
        self.assertEqual(self.feature.room_type.description, "Room with a bed")

    def test_string_representation(self):
        """Test the string representation of the Feature model."""
        self.assertEqual(str(self.feature), 'nothing')
