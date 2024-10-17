from django.test import TestCase
from renthub.models import RoomType, Room, Renter, RentalRequest


class RentalRequestModelTest(TestCase):
    def setUp(self):
        """Set up data for the tests."""
        self.room_type = RoomType.objects.create(type_name="Single Bed",
                                                 description="Room with a bed",
                                                 ideal_for="One person")

        self.room = Room.objects.create(room_number=101,
                                        detail='Demo Room',
                                        price=99.99,
                                        availability=True,
                                        room_type=self.room_type)

        self.renter = Renter.objects.create(username="Pong",
                                            first_name="Pichayoot",
                                            last_name="Tanasinanan",
                                            email="Pongzaza@gmail.com",
                                            phone_number='1234567890')

        self.rental_request = RentalRequest.objects.create(renter=self.renter,
                                                           room=self.room,
                                                           price=self.room.price)

    def test_rental_request_creation(self):
        """Test that the RentalRequest instance can be created successfully."""
        self.assertEqual(str(self.rental_request.renter), 'Pong')
        self.assertEqual(str(self.rental_request.room), "101")
        self.assertEqual(self.rental_request.price, 99.99)

    def test_string_representation(self):
        """Test the string representation of the RentalRequest model."""
        self.assertEqual(str(self.rental_request), "Pong / 101 / 99.99")
