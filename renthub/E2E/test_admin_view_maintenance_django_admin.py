import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class AdminMaintenanceRequestDjangoTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def test_admin_can_view_maintenance_requests_in_admin_panel(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")

        # Step 1: Login
        driver.find_element(By.NAME, "username").send_keys("rhadmin")
        driver.find_element(By.NAME, "password").send_keys("security0")
        driver.find_element(By.XPATH, "//input[@type='submit']").click()

        # Step 2: Wait for Django admin panel and click on "Maintenance requests"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Maintenance requests"))
        )
        driver.find_element(By.LINK_TEXT, "Maintenance requests").click()

        # Step 3: Wait until the request table is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@id='result_list']//tr[2]/th/a"))
        )

        # Now safely fetch the first maintenance request
        first_request = driver.find_element(By.XPATH, "//table[@id='result_list']//tr[2]/th/a").text
        title = driver.find_element(By.XPATH, "//table[@id='result_list']//tr[2]/td[1]").text
        message = driver.find_element(By.XPATH, "//table[@id='result_list']//tr[2]/td[2]").text

        print("First request rental:", first_request)
        print("Title:", title)
        print("Request Message:", message)

        self.assertIn("Room", first_request)
        self.assertTrue("test" in message.lower())

    def test_admin_can_approve_maintenance_request(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")

        # Step 1: Login
        driver.find_element(By.NAME, "username").send_keys("rhadmin")
        driver.find_element(By.NAME, "password").send_keys("security0")
        driver.find_element(By.XPATH, "//input[@type='submit']").click()

        # Step 2: Enter Maintenance requests section
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Maintenance requests"))
        )
        driver.find_element(By.LINK_TEXT, "Maintenance requests").click()

        # Step 3: Wait for table and open the first request
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@id='result_list']//tr[2]/th/a"))
        )
        driver.find_element(By.XPATH, "//table[@id='result_list']//tr[2]/th/a").click()

        # Step 4: Change status to 'approve'
        status_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "status"))
        )
        from selenium.webdriver.support.ui import Select
        Select(status_dropdown).select_by_visible_text("approve")

        # Step 5: Scroll to SAVE and click
        save_button = driver.find_element(By.NAME, "_save")
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "_save")))
        save_button.click()

        # Step 6: Verify success message
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".messagelist li"))
        )
        print("Success:", success_message.text)
        self.assertIn("changed successfully", success_message.text.lower())

    def test_admin_can_reject_maintenance_request(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")

        # Step 1: Login
        driver.find_element(By.NAME, "username").send_keys("rhadmin")
        driver.find_element(By.NAME, "password").send_keys("security0")
        driver.find_element(By.XPATH, "//input[@type='submit']").click()

        # Step 2: Go to Maintenance requests
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Maintenance requests"))
        )
        driver.find_element(By.LINK_TEXT, "Maintenance requests").click()

        # Step 3: Click first request in the list
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@id='result_list']//tr[2]/th/a"))
        )
        driver.find_element(By.XPATH, "//table[@id='result_list']//tr[2]/th/a").click()

        # Step 4: Change status to 'reject'
        status_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "status"))
        )
        from selenium.webdriver.support.ui import Select
        Select(status_dropdown).select_by_visible_text("reject")

        # Step 5: Scroll and click SAVE
        save_button = driver.find_element(By.NAME, "_save")
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "_save")))
        save_button.click()

        # Step 6: Confirm success message
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".messagelist li"))
        )
        print("Success:", success_message.text)
        self.assertIn("changed successfully", success_message.text.lower())

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
