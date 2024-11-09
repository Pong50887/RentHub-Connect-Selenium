"""Test of announcement : Announcement Admin"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from renthub.models import Announcement


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
