from django.test import TestCase
from renthub.models import Renter


class RenterModelTest(TestCase):
    def setUp(self):
        """Set up data for the tests."""
        self.renter = Renter.objects.create(username="Pong",
                                            first_name="Pichayoot",
                                            last_name="Tanasinanan",
                                            email="Pongzaza@gmail.com",
                                            phone_number='1234567890')

    def test_renter_creation(self):
        """Test that the Renter instance can be created successfully."""
        self.assertEqual(self.renter.username, 'Pong')
        self.assertEqual(self.renter.first_name, 'Pichayoot')
        self.assertEqual(self.renter.last_name, 'Tanasinanan')
        self.assertEqual(self.renter.email, 'Pongzaza@gmail.com')
        self.assertEqual(self.renter.phone_number, '1234567890')

    def test_string_representation(self):
        """Test the string representation of the Renter model."""
        self.assertEqual(str(self.renter), self.renter.username)
