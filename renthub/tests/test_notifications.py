from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from ..models import Notification, Renter


class NotificationViewTest(TestCase):

    def setUp(self):
        self.renter = Renter.objects.create_user(username="Pong",
                                                 password='12345')
        login_success = self.client.login(username='Pong', password='12345')
        self.assertTrue(login_success)

        Notification.objects.create(
            renter=self.renter,
            title='Old Notification',
            message='This is an old notification',
            post_date=timezone.now(),
            is_read=True
        )
        Notification.objects.create(
            renter=self.renter,
            title='New Notification',
            message='This is a new notification',
            post_date=timezone.now(),
            is_read=False
        )

    def test_notification_list_view(self):
        # Get the notification page
        self.client.login(username='Pong', password='12345')
        response = self.client.get(reverse('renthub:notifications'))

        # Check if the view loads successfully
        self.assertEqual(response.status_code, 200)

        # Ensure the context contains notifications
        self.assertIn('notifications', response.context)

        # Check the order of notifications
        notifications = response.context['notifications']
        self.assertEqual(notifications[0].title, 'New Notification')  # New should appear first
        self.assertEqual(notifications[1].title, 'Old Notification')

    def test_mark_notifications_as_read(self):
        # Ensure the user is logged in before making the request
        self.client.login(username='Pong', password='12345')  # This line may be unnecessary if login is in setUp

        # Simulate marking notifications as read
        response = self.client.post(reverse('renthub:mark_notifications_read'))

        # Check if the view returns success status
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})

        # Check if the unread notification is now marked as read
        new_notification = Notification.objects.get(title='New Notification')
        self.assertTrue(new_notification.is_read)
