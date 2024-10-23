from django.test import TestCase
from renthub.models import RoomType, Room, Renter, Rental, Transaction
from renthub.utils import Status

class TransactionModelTest(TestCase):
    def setUp(self):
        """Set up data for the tests."""
        self.room_type = RoomType.objects.create(type_name="Single Bed",
                                                 description="Room with a bed",
                                                 ideal_for="One person")

        self.room = Room.objects.create(room_number=101,
                                        detail='Test Room',
                                        price=99.99,
                                        availability=True,
                                        room_type=self.room_type)

        self.renter = Renter.objects.create(username="Pong",
                                            first_name="Pichayoot",
                                            last_name="Tanasinanan",
                                            email="Pongzaza@gmail.com",
                                            phone_number='1234567890')

        self.rental = Rental.objects.create(room=self.room,
                                            renter=self.renter,
                                            rental_fee=99.99)

        self.transaction = Transaction.objects.create(detail="This is ...",
                                                      rental=self.rental,
                                                      date="2024-10-12 14:30:00+00:00",
                                                      status=Status.wait.value)

    def test_transaction_creation(self):
        """Test that the Transaction instance can be created successfully."""
        self.assertEqual(self.transaction.detail, "This is ...")
        self.assertEqual(self.transaction.rental, self.rental)
        self.assertEqual(self.transaction.date, "2024-10-12 14:30:00+00:00")
        self.assertEqual(self.transaction.status, Status.wait.value)

    def test_string_representation(self):
        """Test the string representation of the Transaction model."""
        self.assertEqual(str(self.transaction), Status.wait.value)
