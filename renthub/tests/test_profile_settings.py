import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate
from ..models import Renter
from ..utils import create_temp_image_file


class ProfileSettingsTests(TestCase):
    def setUp(self):
        """
        Set up a test renter and log in.
        """
        self.temp_image = create_temp_image_file()
        self.renter = Renter.objects.create_user(
            username='test_user',
            email='testuser@example.com',
            password='test_password123',
            phone_number='0123456789',
            first_name='Test',
            last_name='User',
            thai_citizenship_id='1234567890123',
            thai_citizenship_id_image=self.temp_image
        )
        self.client.login(username='test_user', password='test_password123')
        self.url = reverse('renthub:profile_settings')
        self.temp_image.seek(0)

    def tearDown(self):
        """Delete temp_image"""
        if hasattr(self, 'temp_image') and os.path.exists(self.temp_image.name):
            os.remove(self.temp_image.name)

    def test_profile_page_access(self):
        """
        Ensure the profile settings page is accessible to logged-in users.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'renthub/profile_settings.html')

    def test_update_profile(self):
        """
        Test updating renter profile information.
        """
        response = self.client.post(self.url, {
            'username': 'updated_user',
            'email': 'updateduser@example.com',
            'phone_number': '0987654321',
            'first_name': 'Test',
            'last_name': 'User',
            'thai_citizenship_id': '2345632454324',
            'thai_citizenship_id_image': self.temp_image,
        }, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.renter.refresh_from_db()
        self.assertEqual(self.renter.username, 'updated_user')
        self.assertEqual(self.renter.email, 'updateduser@example.com')
        self.assertEqual(self.renter.phone_number, '0987654321')

    def test_change_password_success(self):
        """
        Test changing the password with correct inputs.
        """
        response = self.client.post(self.url, {
            'username': 'test_user',
            'email': 'testuser@example.com',
            'phone_number': '0123456789',
            'first_name': 'Test',
            'last_name': 'User',
            'thai_citizenship_id': '2345632454324',
            'thai_citizenship_id_image': self.temp_image,
            'password': 'test_password123',
            'new_password1': 'newpassword456',
            'new_password2': 'newpassword456',
        }, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.renter.refresh_from_db()
        self.client.logout()
        user = authenticate(username=self.renter.username, password='newpassword456')
        self.assertIsNotNone(user)

    def test_change_password_mismatch(self):
        """
        Test changing the password with mismatched new passwords.
        """
        response = self.client.post(self.url, {
            'username': 'test_user',
            'email': 'testuser@example.com',
            'phone_number': '0123456789',
            'first_name': 'Test',
            'last_name': 'User',
            'thai_citizenship_id': '1234567890123',
            'thai_citizenship_id_image': self.temp_image,
            'password': 'test_password123',
            'new_password1': 'newpassword456',
            'new_password2': 'different_password',
        }, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The new passwords do not match.")
        self.renter.refresh_from_db()
        self.assertTrue(self.renter.check_password('test_password123'))

    def test_change_password_invalid_current(self):
        """
        Test changing the password with an incorrect current password.
        """
        response = self.client.post(self.url, {
            'username': 'test_user',
            'email': 'testuser@example.com',
            'phone_number': '0123456789',
            'first_name': 'Test',
            'last_name': 'User',
            'thai_citizenship_id': '1234567890123',
            'thai_citizenship_id_image': self.temp_image,
            'password': 'wrong_password',
            'new_password1': 'newpassword456',
            'new_password2': 'newpassword456',
        }, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The current password is incorrect.")
        self.renter.refresh_from_db()
        self.assertTrue(self.renter.check_password('test_password123'))

    def test_non_logged_in_access(self):
        """
        Ensure non-logged-in users cannot access the profile settings page.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
