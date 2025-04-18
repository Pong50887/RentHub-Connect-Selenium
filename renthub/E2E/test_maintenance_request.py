
import time
from django.test import TestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from mysite import settings
from renthub.utils import kill_port, Browser, start_django_server, log_in, stop_django_server


class MaintenanceRequestTest(TestCase):

    def setUp(self):
        kill_port()
        self.browser = Browser.get_browser()
        self.server_process = start_django_server()


    def test_submit_maintenance_request(self):
        self.browser.get(f"{settings.BASE_URL}/accounts/login/?next=/")

        # Step 1: Log in as renter
        log_in(driver=self.browser, username="demo1", password="hackme11")

        # Step 2: Navigate to maintenance request page
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Contact Us"))
        )
        self.browser.find_element(By.LINK_TEXT, "Contact Us").click()

        # Step 3: Fill and submit the maintenance form
        self.browser.find_element(By.NAME, "title").send_keys("testtt")
        self.browser.find_element(By.NAME, "request_message").send_keys("Wi-Fi has been down since last night.")

        # Step 4: Submit the form
        send_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", send_button)
        time.sleep(0.5)  # give time for animation or sticky nav
        send_button.click()

        # Optional: Check for success alert
        time.sleep(1)
        success_element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.alert li"))
        )

        print("Success message:", success_element.text)
        self.assertIn("maintenance request sent successfully", success_element.text.lower())

    def tearDown(self):
        stop_django_server(self.server_process)
        self.browser.quit()
        kill_port()
