from django.test import TestCase
from django.urls import reverse
from ..models import Renter


class UserProfileViewTest(TestCase):

    def setUp(self):
        self.renter = Renter.objects.create(
            username="testuser",
            email="testuser@example.com",
            phone_number="1234567890",
            thai_citizenship_id="1234567890123"
        )

    def test_user_profile_view_success(self):
        """Test that the user profile page loads successfully."""
        response = self.client.get(reverse('renthub:user_profile', kwargs={'username': self.renter.username}))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'renthub/user_profile.html')

    def test_user_profile_template_display(self):
        """Test that the user profile page displays the renter's information."""
        response = self.client.get(reverse('renthub:user_profile', kwargs={'username': self.renter.username}))

        # Check if the page contains the user profile information
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'testuser@example.com')
        self.assertContains(response, '1234567890')
        self.assertContains(response, '1234567890123')
