from django.test import TestCase
from django.contrib.auth.models import User
from renthub.models import RoomType, Room, Rental, Renter


class RoomTypeModelTest(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(type_name="Single Bed",
                                                 description="Room with a bed",
                                                 ideal_for="One person")

    def test_room_type_creation(self):
        self.assertEqual(self.room_type.type_name, "Single Bed")
        self.assertEqual(self.room_type.description, 'Room with a bed')
        self.assertEqual(self.room_type.ideal_for, "One person")

    def test_string_representation(self):
        self.assertEqual(str(self.room_type), 'Single Bed')


# class RoomModelTest(TestCase):
#     def setUp(self):
#         self.room_type = RoomType.objects.create(type_name="Single Bed",
#                                                  description="Room with a bed",
#                                                  ideal_for="One person")
#         self.room = Room.objects.create(room_number=101, detail='Test Room',
#                                         price=99.99, availability=True, room_type=self.room_type)
#
#     def test_room_creation(self):
#         self.assertEqual(self.room.room_number, 101)
#         self.assertEqual(self.room.detail, 'Test Room')
#         self.assertEqual(self.room.price, 99.99)
#         self.assertEqual(self.room.availability, True)
#         self.assertEqual(self.room.room_type, self.room_type)
#
#     def test_string_representation(self):
#         self.assertEqual(str(self.room), '101')
#
#
# class RenterModelTest(TestCase):
    # def setUp(self):
    #     self.renter = Renter.objects.create(username="Pong",
    #                                         first_name="Pichayoot",
    #                                         last_name="Tanasinanan",
    #                                         email="Pongzaza@gmail.com",
    #                                         phone_number='1234567890')
    #
    # def test_renter_creation(self):
    #     self.assertEqual(self.renter.username, 'Pong')
    #     self.assertEqual(self.renter.username, 'Pichayoot')
    #     self.assertEqual(self.renter.username, 'Tanasinanan')
    #     self.assertEqual(self.renter.username, 'Pongzaza@gmail.com')
    #     self.assertEqual(self.renter.phone_number, '1234567890')


# class RentalModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='johndoe', password='password123')
#         self.renter = Renter.objects.create(user=self.user, phone_number='1234567890')
#         self.room = Room.objects.create(room_number='102', description='Sample Room')
#         self.rental = Rental.objects.create(room=self.room, renter=self.renter)
#
#     def test_rental_creation(self):
#         self.assertEqual(self.rental.room.room_number, '102')
#         self.assertEqual(self.rental.renter.user.username, 'johndoe')
