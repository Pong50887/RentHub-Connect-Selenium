from django.test import TestCase
from django.contrib.auth.models import User
from renthub.models import RoomType, Room, Renter, Rental


class RentalModelTest(TestCase):
    def setUp(self):
        """Set up data for the tests."""
        self.room_type = RoomType.objects.create(type_name="Single Bed",
                                                 description="Room with a bed",
                                                 ideal_for="One person")

        self.room = Room.objects.create(room_number=101,
                                        detail='Demo Room',
                                        price=99.99,
                                        room_type=self.room_type)

        self.renter = Renter.objects.create(username="Pong",
                                            first_name="Pichayoot",
                                            last_name="Tanasinanan",
                                            email="Pongzaza@gmail.com",
                                            phone_number='1234567890')

        self.rental = Rental.objects.create(room=self.room,
                                            renter=self.renter,
                                            price=self.room.price)

        self.admin = User.objects.create_user(username="admin",
                                              email="admin@gmail.com",
                                              password="adminpass")

    def test_rental_creation(self):
        """Test that the Rental instance can be created successfully."""
        self.assertEqual(str(self.rental.room), "Room 101 - Demo Room")
        self.assertEqual(str(self.rental.renter), "Pong")
        self.assertEqual(self.rental.price, 99.99)

    def test_renter_can_create_rental(self):
        """A renter can create a rental."""
        rental = Rental.objects.create(room=self.room, renter=self.renter, price=self.room.price)
        self.assertIsInstance(rental, Rental)
        self.assertEqual(rental.renter, self.renter)

    def test_non_renter_cannot_create_rental(self):
        """A non-renter cannot create a rental."""
        with self.assertRaises(Exception):
            Rental.objects.create(room=self.room, renter=self.admin, price=self.room.price)
