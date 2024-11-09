from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from ...models import MaintenanceRequest, Rental, Room, Renter, RoomType
from ...utils import Status


class MaintenanceRequestModelTest(TestCase):
    """Tests for the MaintenanceRequest model."""

    def setUp(self):
        """Set up test data for MaintenanceRequest model tests."""
        self.room_type = RoomType.objects.create(
            type_name="Single Bed Room",
            description="A single room ideal for solo travelers",
            ideal_for="Solo",
            image=None
        )

        self.room = Room.objects.create(
            room_number=101,
            detail="Single room with garden view",
            price=3000.00,
            room_type=self.room_type
        )

        self.renter = Renter.objects.create_user(
            username="johndoe",
            password="password123",
            phone_number="0123456789"
        )

        self.rental = Rental.objects.create(
            room=self.room,
            renter=self.renter,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            price=3000.00,
            is_paid=True,
        )

    def test_create_maintenance_request(self):
        """Test creating a MaintenanceRequest instance with valid data."""
        maintenance_request = MaintenanceRequest.objects.create(
            rental=self.rental,
            request_message="Leaky faucet needs repair.",
            title="Faucet Repair",
            date_requested=timezone.now()
        )

        self.assertEqual(maintenance_request.rental, self.rental)
        self.assertEqual(maintenance_request.request_message, "Leaky faucet needs repair.")
        self.assertEqual(maintenance_request.title, "Faucet Repair")
        self.assertEqual(maintenance_request.status, Status.wait)
        self.assertIsNotNone(maintenance_request.date_requested)

    def test_string_representation(self):
        """Test the string representation of a MaintenanceRequest instance."""
        maintenance_request = MaintenanceRequest.objects.create(
            rental=self.rental,
            request_message="Leaky faucet needs repair.",
            title="Faucet Repair",
            date_requested=timezone.now()
        )
        expected_str = f"Request by {self.rental.renter} for {self.rental.room}"
        self.assertEqual(str(maintenance_request), expected_str)
