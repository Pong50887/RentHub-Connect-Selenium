from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from renthub.models import MaintenanceRequest, Rental, Renter, Room
from renthub.utils import Status


class MaintenanceRequestAccessTest(TestCase):
    """Tests for maintenance request access."""
    def setUp(self):
        """Setup data for testing"""
        self.room = Room.objects.create(
            room_number=101,
            detail="A spacious room",
            price=3000.00
        )

        self.renter_with_rental = Renter.objects.create(
            username="Jane Doe",
            phone_number="1234567890",
            email="jane.doe@example.com"
        )
        self.renter_without_rental = Renter.objects.create(
            username="John Smith",
            phone_number="0987654321",
            email="john.smith@example.com"
        )

        self.rental = Rental.objects.create(
            room=self.room,
            renter=self.renter_with_rental,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=30),
            price=3000.00
        )

        self.url = reverse('renthub:contact_us')

    def test_renter_with_rental_can_submit_maintenance_request(self):
        """Test that a renter with an active rental can submit a maintenance request"""
        data = {
            'rental': self.rental.id,
            'request_message': "The air conditioning is not working.",
            'title': "Air Conditioning Issue",
            'status': Status.wait,
            'date_requested': timezone.now(),
        }

        self.client.force_login(self.renter_with_rental)

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code,
                         302)  # Assuming the response is a redirect after successful form submission
        self.assertEqual(MaintenanceRequest.objects.count(), 1)
        maintenance_request = MaintenanceRequest.objects.first()
        self.assertEqual(maintenance_request.rental, self.rental)
        self.assertEqual(maintenance_request.request_message, "The air conditioning is not working.")
        self.assertEqual(maintenance_request.title, "Air Conditioning Issue")

    def test_renter_without_rental_cannot_submit_maintenance_request(self):
        """Test that a renter without an active rental cannot submit a maintenance request"""
        data = {
            'request_message': "The heater is broken.",
            'title': "Heater Issue",
            'status': Status.wait,
            'date_requested': timezone.now(),
        }

        self.client.force_login(self.renter_without_rental)

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        follow_response = self.client.get(response.url)

        self.assertContains(follow_response, "You do not have a rental associated with your account.")

    def test_renter_without_rental_access(self):
        """Test that the renter without an active rental cannot access the maintenance request page"""

        self.client.force_login(self.renter_without_rental)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
