"""Test of announcement : Announcement in Home view"""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from renthub.models import Renter, Announcement


class AnnouncementHomeViewTest(TestCase):
    """Tests of Announcement in home page."""

    def setUp(self):
        """Set up data for the tests."""
        self.renter = Renter.objects.create_user(username="Pong",
                                                 password='12345')
        login_success = self.client.login(username='Pong', password='12345')
        self.assertTrue(login_success)

        self.announcement = Announcement.objects.create(
            title="First Announcement",
            content="This is the first announcement.",
            publish_date=timezone.now()
        )

    def test_home_view_announcement_content(self):
        """Test if the announcement is rendered correctly on the home page"""
        url = reverse('renthub:home')
        response = self.client.get(url)

        self.assertContains(response, self.announcement.title)

    def test_home_view_multiple_announcements(self):
        """Test if multiple announcements are rendered correctly on the home page"""
        second_announcement = Announcement.objects.create(
            title="Second Announcement",
            content="This is the second announcement.",
            publish_date=timezone.now()
        )

        url = reverse('renthub:home')
        response = self.client.get(url)

        self.assertContains(response, self.announcement.title)
        self.assertContains(response, second_announcement.title)
