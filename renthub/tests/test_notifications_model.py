from django.test import TestCase
from django.utils import timezone
from ..models import Notification, Renter

class NotificationModelTest(TestCase):

    def setUp(self):
        self.renter = Renter.objects.create_user(username="Pong",
                                            first_name="Pichayoot",
                                            last_name="Tanasinanan",
                                            email="Pongzaza@gmail.com",
                                            phone_number='1234567890')

    def test_notification_creation(self):
        notification = Notification.objects.create(
            renter=self.renter,
            title='Test Notification',
            message='This is a test message',
            post_date=timezone.now(),
        )

        self.assertEqual(notification.title, 'Test Notification')
        self.assertEqual(notification.message, 'This is a test message')
        self.assertEqual(notification.renter, self.renter)
        self.assertFalse(notification.is_read)

    def test_mark_as_read(self):
        notification = Notification.objects.create(
            renter=self.renter,
            title='Unread Notification',
            message='Unread message',
            post_date=timezone.now(),
        )

        notification.is_read = True
        notification.save()
        self.assertTrue(notification.is_read)
