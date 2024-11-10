from django.test import TestCase
from django.urls import reverse
from ..models import Room, RoomType


class SearchAndFilterTest(TestCase):
    """Tests for room search, filter, and sorting functionality."""

    def setUp(self):
        """Sets up test data for rooms and room types."""
        self.room_type_1 = RoomType.objects.create(type_name="Studio", description="A small studio room.")
        self.room_type_2 = RoomType.objects.create(type_name="Double Bed Room",
                                                   description="A spacious double bed room.")
        self.start_date = "2023-01"
        self.end_date = "2023-03"

        self.room_1 = Room.objects.create(
            room_number=101,
            detail="A quiet studio room.",
            price=4500.00,
            room_type=self.room_type_1
        )
        self.room_2 = Room.objects.create(
            room_number=102,
            detail="A large double bed room.",
            price=5500.00,
            room_type=self.room_type_2
        )

    def test_search_filter_and_availability(self):
        """Tests room search and filtering by type and availability."""
        search_query = "studio"
        room_type_id = self.room_type_1.id

        response = self.client.get(reverse("renthub:room_list"), {
            "search": search_query,
            "room_type": room_type_id,
            "start_month": self.start_date,
            "end_month": self.end_date
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.room_1, response.context["rooms"])
        self.assertNotIn(self.room_2, response.context["rooms"])

    def test_sorting_by_price(self):
        """Tests room sorting by ascending and descending price."""
        response1 = self.client.get(reverse("renthub:room_list"), {
            "sort": "price_asc",
            "start_month": self.start_date,
            "end_month": self.end_date
        })
        rooms1 = response1.context["rooms"]
        self.assertTrue(rooms1[0].price < rooms1[1].price)

        response2 = self.client.get(reverse("renthub:room_list"), {
            "sort": "price_desc",
            "start_month": self.start_date,
            "end_month": self.end_date
        })
        rooms2 = response2.context["rooms"]
        self.assertTrue(rooms2[0].price > rooms2[1].price)
