from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from ..models import Room, RoomType


class SearchAndFilterTest(TestCase):
    """Tests for room search, filter, and sorting functionality."""

    def setUp(self):
        """Sets up test data for rooms and room types."""
        self.room_type_1 = RoomType.objects.create(type_name="Studio", description="A small studio room.")
        self.room_type_2 = RoomType.objects.create(type_name="Double Bed Room",
                                                   description="A spacious double bed room.")
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
        with patch('renthub.models.Room.is_available', return_value=True):
            search_query = "studio"
            room_type_id = self.room_type_1.id

            response = self.client.post(reverse("renthub:room_list"), {
                "search": search_query,
                "room_type": room_type_id
            })

            self.assertEqual(response.status_code, 200)
            rooms = response.context["rooms"]
            self.assertIn(self.room_1, rooms)
            self.assertNotIn(self.room_2, rooms)

    def test_sorting_by_price(self):
        """Tests room sorting by ascending and descending price."""
        with patch('renthub.models.Room.is_available', return_value=True):
            response_asc = self.client.post(reverse("renthub:room_list"), {
                "sort": "price_asc"
            })
            rooms_asc = list(response_asc.context["rooms"])
            self.assertEqual(rooms_asc[0], self.room_1)
            self.assertEqual(rooms_asc[1], self.room_2)

            response_desc = self.client.post(reverse("renthub:room_list"), {
                "sort": "price_desc"
            })
            rooms_desc = list(response_desc.context["rooms"])
            self.assertEqual(rooms_desc[0], self.room_2)
            self.assertEqual(rooms_desc[1], self.room_1)
