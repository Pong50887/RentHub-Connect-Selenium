from django.test import TestCase
from renthub.models import Announcement


class AnnouncementModelTest(TestCase):
    def setUp(self):
        """Set up data for the tests."""
        self.announcement = Announcement.objects.create(title="Emergency",
                                                        content="There is a cockroach army at the lobby",
                                                        publish_date="2024-10-12 14:30:00+00:00")

    def test_announcement_creation(self):
        """Test that the Announcement instance can be created successfully."""
        self.assertEqual(self.announcement.title, "Emergency")
        self.assertEqual(self.announcement.content, "There is a cockroach army at the lobby")
        self.assertEqual(self.announcement.publish_date, "2024-10-12 14:30:00+00:00")

    def test_string_representation(self):
        """Test the string representation of the Announcement model."""
        self.assertEqual(str(self.announcement), "Emergency")
