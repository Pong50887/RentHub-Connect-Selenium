# """Tests of booking: rental cancellation."""
#
# from django.test import TestCase
# from django.urls import reverse
# from renthub.models import Rental, Room, Renter
#
#
# class PaymentCancelTests(TestCase):
#     """Tests of payment cancellation method."""
#
#     def setUp(self):
#         """Set up data for the tests."""
#         self.renter = Renter.objects.create(username="normal_user", password="test123", phone_number="1234567890")
#         self.renter1 = Renter.objects.create(username="normal_user1", password="test123", phone_number="1234567890")
#         self.renter2 = Renter.objects.create(username="normal_user2", password="test123", phone_number="1234567890")
#         self.room = Room.objects.create(room_number="101", detail='A cozy room', price=1000.00)
#
#     def test_renter_can_cancel_rental(self):
#         """A renter can cancel their own rental."""
#         self.client.force_login(self.renter)
#         rental = Rental.objects.create(room=self.room, renter=self.renter, price=self.room.price)
#         response = self.client.post(reverse('renthub:cancel', args=[self.room.room_number]), follow=True)
#         self.assertFalse(Rental.objects.filter(id=rental.id).exists())
#         self.room.refresh_from_db()
#         self.assertContains(response, "Your booking cancellation was successful.")
#
#     def test_renter_cannot_cancel_other_renters_rental(self):
#         """A renter cannot cancel another renter's rental."""
#         self.client.force_login(self.renter1)
#         rental = Rental.objects.create(room=self.room, renter=self.renter1, price=self.room.price)
#         self.client.force_login(self.renter2)
#         response = self.client.post(reverse('renthub:cancel', kwargs={'room_number': self.room.room_number}),
#                                     follow=True)
#         self.assertTrue(Rental.objects.filter(id=rental.id).exists())
#         self.assertContains(response, "You do not have an active booking for this room.")
