"""Tests of booking: DetailView changes related to booking feature."""

from django.test import TestCase
from django.urls import reverse

from mysite import settings

from renthub.utils import Browser, kill_port, stop_django_server, start_django_server


class RoomDetailViewTests(TestCase):
    """Tests of DetailView."""

    def setUp(self):
        """Set up data for the tests."""
        kill_port()
        self.server_process = start_django_server()
        self.browser = Browser.get_logged_in_browser(username='demo4', password='hackme44')

    def tearDown(self):
        """Clean up after tests."""
        stop_django_server(self.server_process)
        self.browser.quit()
        kill_port()

    def test_non_existent_room(self):
        """Accessing a non-existent room redirects renter to home page."""
        self.browser.get(f'{settings.BASE_URL}{reverse("renthub:room", kwargs={"room_number": 999})}')
        self.assertEqual(self.browser.current_url, f'{settings.BASE_URL}{reverse("renthub:home")}')
        self.assertIn("Welcome", self.browser.page_source)

    def test_renter_can_rent_available_room(self):
        """A renter can access an available room."""
        self.browser.get(f'{settings.BASE_URL}'
                         f'{reverse("renthub:room", 
                                    kwargs={"room_number": 208})}')
        self.assertIn("Proceed with Rental", self.browser.page_source)
