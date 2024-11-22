"""Test of announcement : Announcement view"""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import date_format

import unittest

from renthub.models import Announcement


class AnnouncementDetailViewTest(TestCase):
    """Tests of announcement page."""

    def setUp(self):
        """Set up data for the tests."""
        self.announcement = Announcement.objects.create(
            title="Test Announcement",
            content="This is a test announcement.",
            publish_date=timezone.now()
        )

    def test_announcement_view_status_code(self):
        """Test if the detail view returns a 200 status code"""
        url = reverse('renthub:announcement', kwargs={'pk': self.announcement.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_announcement_view_template(self):
        """Test if the correct template is used"""
        url = reverse('renthub:announcement', kwargs={'pk': self.announcement.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'renthub/announcement.html')

    def test_announcement_view_content(self):
        """Test if the announcement details are rendered correctly with Asia/Bangkok timezone."""
        url = reverse('renthub:announcement', kwargs={'pk': self.announcement.pk})
        response = self.client.get(url)

        self.assertContains(response, self.announcement.title)
        self.assertContains(response, self.announcement.content)

        publish_date_bangkok = timezone.localtime(self.announcement.publish_date, timezone.get_fixed_timezone(7 * 60))
        formatted_publish_date = date_format(publish_date_bangkok, "F j, Y")

        self.assertContains(response, formatted_publish_date)
