"""Test of renting: only renters can rent."""
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mysite import settings
from mysite.settings import ADMIN_USERNAME, ADMIN_PASSWORD
from renthub.utils import kill_port, Browser, admin_login
from django.test import TestCase


class RentingTests(TestCase):
    """Tests of Renting Cases."""

    def setUp(self):
        """Set up data for the tests."""
        kill_port()
        self.browser = Browser.get_browser()
        Browser.start_django_server()

    def tearDown(self) -> None:
        """Clean up after tests."""
        Browser.stop_django_server()
        self.browser.quit()
        kill_port()

    def renting(self):
        """A user renting from room details page."""
        proceed_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-bs-target='#exampleModalLong']")))
        ActionChains(self.browser).move_to_element(proceed_button).perform()

        proceed_button.click()

        checkbox = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, "agreeTerms")))
        ActionChains(self.browser).move_to_element(checkbox).perform()

        checkbox.click()
        confirm_button = self.browser.find_element(By.ID, "confirmAgreement")
        confirm_button.click()

    def test_unauthorized_user_renting(self):
        """An unauthorized user is redirected to log in page when they try to rent."""
        self.browser.get(f"{settings.BASE_URL}/room/210")
        self.renting()
        self.assertIn("login", self.browser.current_url)

    def test_logged_in_renter_renting(self):
        """A logged in renter can rent."""
        Browser.log_in(driver=self.browser, username="demo4", password="hackme44")
        self.browser.get(f"{settings.BASE_URL}/room/210")
        self.renting()
        self.assertIn("payment", self.browser.current_url)

    def test_logged_in_admin_renting(self):
        """Any logged in user who are not renter can't rent : admin."""
        Browser.log_in(driver=self.browser, username=ADMIN_USERNAME, password=ADMIN_PASSWORD)
        self.browser.get(f"{settings.BASE_URL}/room/210")
        self.renting()
        self.assertNotIn("payment", self.browser.current_url)

    def test_logged_in_property_owner_renting(self):
        """Any logged in user who are not renter can't rent : property owner."""
        Browser.log_in(driver=self.browser, username="renthub1", password="owner123")
        self.browser.get(f"{settings.BASE_URL}/room/210")
        self.renting()
        self.assertNotIn("payment", self.browser.current_url)
