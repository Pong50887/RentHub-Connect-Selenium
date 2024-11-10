from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from renthub.models import Notification, Renter


class NotificationAdminTest(TestCase):
    """Tests for admin management of Notification(s)."""

    def setUp(self):
        """Set up data for the tests, including an admin user and a test renter."""
        # Create an admin user
        self.admin_user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        self.client.login(username='admin', password='admin')

        # Create a test renter
        self.renter = Renter.objects.create_user(username="TestRenter", password="password")

    def test_notification_admin_access(self):
        """Test if the Notification model is accessible in admin."""
        response = self.client.get(reverse('admin:renthub_notification_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_notification_creation_via_admin(self):
        """Test creating a notification via the admin."""
        response = self.client.post(reverse('admin:renthub_notification_add'), {
            'renter': self.renter.id,
            'title': 'Admin Created Notification',
            'message': 'This notification was created through the admin.',
            'post_date_0': timezone.now().strftime('%Y-%m-%d'),
            'post_date_1': timezone.now().strftime('%H:%M:%S'),
            'is_read': False
        })

        # Verify that the request was successful (redirected to change list)
        self.assertEqual(response.status_code, 302)
        # Check if the notification was created
        self.assertTrue(Notification.objects.filter(title='Admin Created Notification').exists())
