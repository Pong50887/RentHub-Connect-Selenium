import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class RentingValidationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def test_renter_cannot_rent_same_room_twice(self):
        driver = self.driver
        driver.get("http://localhost:8000/accounts/login/")

        # Step 1: Login
        driver.find_element(By.NAME, "username").send_keys("demo4")
        driver.find_element(By.NAME, "password").send_keys("hackme44")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Step 2: Try to rent a room already rented
        driver.get("http://localhost:8000/room/105/")

        # Step 3: Check for alert message instead of Rent button
        alert = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        self.assertIn("not available", alert.text.lower())

    def test_renting_requires_terms_checkbox(self):
        driver = self.driver
        driver.get("http://localhost:8000/accounts/login/")

        # Step 1: Login
        driver.find_element(By.NAME, "username").send_keys("demo4")
        driver.find_element(By.NAME, "password").send_keys("hackme44")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Step 2: Click "Rooms" in navbar
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Rooms"))
        ).click()

        # Step 3: Click "View Details" for the first available room
        view_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View Details')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", view_btn)
        view_btn.click()

        # Step 4: Click "Proceed with Rental" without ticking the checkbox
        proceed_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Proceed with Rental')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", proceed_btn)
        driver.execute_script("arguments[0].click();", proceed_btn)

        # Step 5: Try to click "Confirm Agreement" without agreeing to terms
        confirm_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm Agreement')]"))
        )
        confirm_btn.click()

        # Step 6: Assert checkbox shows red border or error
        error_label = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'agree to the terms')]"))
        )
        self.assertIn("agree", error_label.text.lower())

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
