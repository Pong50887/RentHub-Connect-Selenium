import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MaintenanceRequestTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def test_submit_maintenance_request(self):
        driver = self.driver
        driver.get("http://localhost:8000/accounts/login/?next=/")

        # Step 1: Log in as renter
        driver.find_element(By.NAME, "username").send_keys("demo1")
        driver.find_element(By.NAME, "password").send_keys("hackme11")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Step 2: Navigate to maintenance request page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Contact Us"))
        )
        driver.find_element(By.LINK_TEXT, "Contact Us").click()

        # Step 3: Fill and submit the maintenance form
        driver.find_element(By.NAME, "title").send_keys("testtt")
        driver.find_element(By.NAME, "request_message").send_keys("Wi-Fi has been down since last night.")

        # Step 4: Submit the form
        send_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
        time.sleep(0.5)  # give time for animation or sticky nav
        send_button.click()

        # Optional: Check for success alert
        time.sleep(1)
        success_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.alert li"))
        )

        print("Success message:", success_element.text)
        self.assertIn("maintenance request sent successfully", success_element.text.lower())

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
