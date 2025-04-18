
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mysite import settings
from renthub.utils import kill_port, Browser, log_in, start_django_server, stop_django_server
from django.test import TestCase

class RentingValidationTest(TestCase):

    def setUp(self):
        kill_port()
        self.browser = Browser.get_browser()
        self.server_process = start_django_server()

    def test_renter_cannot_rent_same_room_twice(self):
        # Step 1: Login
        log_in(driver=self.browser, username="demo4", password="hackme44")

        # Step 2: Try to rent a room already rented
        self.browser.get(f"{settings.BASE_URL}/room/105/")

        # Step 3: Check for alert message instead of Rent button
        alert = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        self.assertIn("not available", alert.text.lower())

    def test_renting_requires_terms_checkbox(self):
        # Step 1: Login
        log_in(driver=self.browser, username="demo4", password="hackme44")

        # Step 2: Click "Rooms" in navbar
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Rooms"))
        ).click()

        # Step 3: Click "View Details" for the first available room
        view_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View Details')]"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", view_btn)
        view_btn.click()

        # Step 4: Click "Proceed with Rental" without ticking the checkbox
        proceed_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Proceed with Rental')]"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", proceed_btn)
        self.browser.execute_script("arguments[0].click();", proceed_btn)

        # Step 5: Try to click "Confirm Agreement" without agreeing to terms
        confirm_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm Agreement')]"))
        )
        confirm_btn.click()

        # Step 6: Assert checkbox shows red border or error
        error_label = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'agree to the terms')]"))
        )
        self.assertIn("agree", error_label.text.lower())

    def tearDown(self):
        stop_django_server(self.server_process)
        self.browser.quit()
        kill_port()
