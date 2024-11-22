from django.test import TestCase
from django.urls import reverse
from ..models import Renter
from django.contrib.auth.models import User


class UserProfileViewTest(TestCase):

    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="password123"
        )

        # Create a normal user
        self.normal_user = User.objects.create_user(
            username="normaluser",
            email="normal@example.com",
            password="password123"
        )

        self.renter = Renter.objects.create(
            username="testuser",
            email="testuser@example.com",
            phone_number="1234567890",
            thai_citizenship_id="1234567890123"
        )

    def test_superuser_access_user_profile_view(self):
        """Test that superusers can access the user profile page."""
        # Log in as superuser
        self.client.login(username="adminuser", password="password123")

        # Access the user profile page
        response = self.client.get(reverse('renthub:user_profile', kwargs={'username': self.renter.username}))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'renthub/user_profile.html')

    def test_non_superuser_redirected_to_home(self):
        """Test that non-superusers are redirected to the home page."""
        # Log in as a normal user
        self.client.login(username="normaluser", password="password123")

        # Access the user profile page
        response = self.client.get(reverse('renthub:user_profile', kwargs={'username': self.renter.username}))

        # Check if the user is redirected
        self.assertRedirects(response, reverse('renthub:home'))

    def test_unauthenticated_user_redirected_to_login(self):
        """Test that unauthenticated users are redirected to the login page."""
        # Access the user profile page without logging in
        response = self.client.get(reverse('renthub:user_profile', kwargs={'username': self.renter.username}))

        # Check if the user is redirected to the login page
        self.assertRedirects(response,
                             f"{reverse('login')}?next="
                             f"{reverse('renthub:user_profile', kwargs={'username': self.renter.username})}")
