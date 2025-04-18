import os

from django.test import TestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mysite import settings
from renthub.utils import Browser, kill_port, admin_login, start_django_server, stop_django_server


class PaymentValidationTest(TestCase):

    def setUp(self):
        kill_port()
        self.server_process = start_django_server()
        self.browser = Browser.get_browser()

    def test_upload_non_image_slip(self):
        driver = self.browser
        driver.get(f"{settings.BASE_URL}/accounts/login/")

        # Step 1: Login
        driver.find_element(By.NAME, "username").send_keys("demo3")
        driver.find_element(By.NAME, "password").send_keys("hackme33")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Step 2: Go to My Rentals
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "My Rentals"))
        ).click()

        # Step 3: Click Pay Rental
        pay_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Pay Rental')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", pay_button)
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Pay Rental')]")))
        pay_button.click()

        # Step 4: Upload a non-image file
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "payment_slip"))
        )
        non_image_path = os.path.abspath("renthub/E2E/test_assets/example.txt")
        upload_input.send_keys(non_image_path)

        # Step 5: Scroll to and click Send using JS
        send_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", send_button)
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send')]")))
        driver.execute_script("arguments[0].click();", send_button)

        # Step 6: Expect error or rejection
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.alert li"))
        ).text

        print("Upload Error Message:", error_message)
        self.assertIn("no payment slip uploaded", error_message.lower())

    def tearDown(self):
        stop_django_server(self.server_process)
        self.browser.quit()
        kill_port()
