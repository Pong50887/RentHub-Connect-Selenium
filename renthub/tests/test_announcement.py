"""Test of announcement."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.formats import date_format

from renthub.models import Announcement
import unittest


class AnnouncementAdminTest(TestCase):
    """Tests of admin management of Announcement(s)."""

    def setUp(self):
        """Set up data for the tests."""
        self.admin_user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        self.client.login(username='admin', password='admin')

    def test_announcement_admin_access(self):
        """Test if the Announcement model is accessible in admin"""
        response = self.client.get(reverse('admin:renthub_announcement_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_announcement_creation_via_admin(self):
        """Test creating an announcement via the admin"""
        response = self.client.post(reverse('admin:renthub_announcement_add'), {
            'title': 'Admin Created Announcement',
            'content': 'This announcement was created through the admin.',
            'publish_date_0': timezone.now().strftime('%Y-%m-%d'),
            'publish_date_1': timezone.now().strftime('%H:%M:%S')
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Announcement.objects.filter(title='Admin Created Announcement').exists())


class AnnouncementHomeViewTest(TestCase):
    """Tests of Announcement in home page."""

    def setUp(self):
        """Set up data for the tests."""
        self.announcement = Announcement.objects.create(
            title="First Announcement",
            content="This is the first announcement.",
            publish_date=timezone.now()
        )

    def test_home_view_announcement_content(self):
        """Test if the announcement is rendered correctly on the home page"""
        url = reverse('renthub:home')
        response = self.client.get(url)

        self.assertContains(response, self.announcement)

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

    @unittest.skip("fix later before release")
    def test_announcement_view_content(self):
        """Test if the announcement details are rendered correctly with Asia/Bangkok timezone."""
        url = reverse('renthub:announcement', kwargs={'pk': self.announcement.pk})
        response = self.client.get(url)

        self.assertContains(response, self.announcement.title)
        self.assertContains(response, self.announcement.content)

        publish_date_bangkok = timezone.localtime(self.announcement.publish_date, timezone.get_fixed_timezone(7 * 60))
        formatted_publish_date = date_format(publish_date_bangkok, "N j, Y, P")

        self.assertContains(response, formatted_publish_date)
