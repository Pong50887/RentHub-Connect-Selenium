"""Tests of booking: PaymentListView changes related to booking feature."""

from django.test import TestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mysite import settings
from renthub.utils import Browser, kill_port, admin_login


class PaymentListViewTests(TestCase):
    """Tests of PaymentListView."""

    def setUp(self):
        """Set up data for the tests."""
        kill_port()
        Browser.start_django_server()
        self.browser = Browser.get_browser()

        admin_login(self.browser)

        self.browser.get(f"{settings.BASE_URL}/admin/renthub/rental/add")
        room_select = Select(self.browser.find_element(By.ID, 'id_room'))
        for option in room_select.options:
            if '207' in option.text:
                room_select.select_by_visible_text(option.text)
                break
        renter_select = Select(self.browser.find_element(By.ID, 'id_renter'))
        renter_select.select_by_visible_text('demo4')
        price_field = self.browser.find_element(By.ID, 'id_price')
        price_field.send_keys(100)

        save_button = self.browser.find_element(By.NAME, '_save')
        save_button.click()

    def tearDown(self) -> None:
        """Clean up after tests."""
        self.browser.get(f"{settings.BASE_URL}/admin/renthub/rental/")
        rows = self.browser.find_elements(By.CSS_SELECTOR, 'tr')
        for row in rows:
            if '207' in row.text:
                target_row = row
                break
        checkbox = target_row.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
        checkbox.click()
        action_dropdown = self.browser.find_element(By.NAME, 'action')
        action_dropdown.click()
        action_dropdown.find_element(By.XPATH, '//option[@value="delete_selected"]').click()
        go_button = self.browser.find_element(By.NAME, 'index')
        go_button.click()

        confirm_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="submit"][value="Yes, I’m sure"]'))
        )
        confirm_button.click()

        Browser.stop_django_server()
        self.browser.quit()
        kill_port()

    def test_no_rental_message_for_renter_without_rentals(self):
        """A renter without any rental sees that their payment list page is empty."""
        self.browser1 = Browser.get_logged_in_browser(username='demo5', password='hackme55')

        self.browser1.get(f"{settings.BASE_URL}{reverse('renthub:payment_list')}")
        page_source = self.browser1.page_source
        self.assertIn("You currently have no ongoing rentals.", page_source)

        self.browser1.quit()

    def test_rental_display_for_renter_with_rentals(self):
        """A renter with any rental sees all of their existing rental(s) in their payment list page."""
        self.browser1 = Browser.get_logged_in_browser(username='demo4', password='hackme44')

        self.browser1.get(f"{settings.BASE_URL}{reverse('renthub:payment_list')}")
        page_source = self.browser1.page_source
        self.assertIn("207", page_source)

        self.browser1.quit()
