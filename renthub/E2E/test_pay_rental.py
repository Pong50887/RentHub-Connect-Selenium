import unittest
import os

from django.template.defaultfilters import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class PaymentFlowTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def test_user_can_submit_rental_payment(self):
        driver = self.driver
        driver.get("http://localhost:8000/accounts/login/")

        # Step 1: Login
        driver.find_element(By.NAME, "username").send_keys("demo4")
        driver.find_element(By.NAME, "password").send_keys("hackme44")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Step 2: Click "My Rentals"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "My Rentals"))
        ).click()

        # Step 3: Click "Pay Rental" button
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Pay Rental')]"))
        )

        pay_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Pay Rental')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", pay_button)
        pay_button.click()

        # Step 4: Upload payment slip
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "payment_slip"))
        )

        # Scroll into view before uploading
        driver.execute_script("arguments[0].scrollIntoView(true);", upload_input)

        # Absolute path for the image
        slip_path = r"D:\Users\picha\Desktop\Github\RentHub-Connect\media\profile_images\image.jpg"
        upload_input.send_keys(slip_path)

        # Step 5: Click Send
        send_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", send_button)
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send')]")))
        driver.execute_script("arguments[0].click();", send_button)  # Use JS to avoid visual overlap

        # Step 6: Assert success message on homepage
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.alert"))
        )
        success_message = driver.find_element(By.XPATH, "//ul[contains(@class, 'alert')]/li").text
        print("Payment Success:", success_message)
        self.assertIn("your rental request was submitted successfully", success_message.lower())

    def test_payment_button_disappears_after_submit(self):
        driver = self.driver
        driver.get("http://localhost:8000/accounts/login/")

        # Step 1: Login
        driver.find_element(By.NAME, "username").send_keys("demo4")
        driver.find_element(By.NAME, "password").send_keys("hackme44")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Step 2: Click "My Rentals" (wait + locate + click separately)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "My Rentals"))
        )
        driver.find_element(By.LINK_TEXT, "My Rentals").click()

        # Step 3: Wait for the button and verify it says "View Details"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "view-detail-btn"))
        )
        button_text = driver.find_element(By.CLASS_NAME, "view-detail-btn").text
        print("Button text after payment:", button_text)
        self.assertIn("view details", button_text.lower())

    def test_user_cannot_submit_without_slip(self):
        driver = self.driver
        driver.get("http://localhost:8000/accounts/login/")
        driver.find_element(By.NAME, "username").send_keys("demo4")
        driver.find_element(By.NAME, "password").send_keys("hackme44")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Step 1: Go to My Rentals
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "My Rentals"))
        ).click()

        # Step 2: Click "Pay Rental"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Pay Rental')]"))
        ).click()

        # Step 3: Scroll and try to submit without selecting a file
        send_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Send')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", send_button)
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send')]")))
        driver.execute_script("arguments[0].click();", send_button)

        # Step 4: Verify the alert message appears
        alert_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'alert')]/li"))
        ).text
        print("Validation Message:", alert_message)
        self.assertIn("no payment slip uploaded", alert_message.lower())

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
