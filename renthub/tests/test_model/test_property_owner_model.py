from django.test import TestCase
from ...models import PropertyOwner


class PropertyOwnerModelTest(TestCase):
    """Test suite for the PropertyOwner model."""

    def setUp(self):
        """Set up a PropertyOwner instance for testing."""
        self.property_owner = PropertyOwner.objects.create_user(
            username="owner_user",
            password="password123",
            location="123 Property St, City ville",
            phone_number="1234567890",
            is_superuser=True
        )

    def test_property_owner_creation(self):
        """Test the successful creation of a PropertyOwner instance."""
        self.assertEqual(self.property_owner.username, "owner_user")
        self.assertEqual(self.property_owner.location, "123 Property St, City ville")
        self.assertEqual(self.property_owner.phone_number, "1234567890")
        self.assertTrue(self.property_owner.is_superuser)

    def test_string_representation(self):
        """Test the string representation of a PropertyOwner instance."""
        expected_str = f"Username: {self.property_owner.username}, Phone: {self.property_owner.phone_number}"
        self.assertEqual(str(self.property_owner), expected_str)
