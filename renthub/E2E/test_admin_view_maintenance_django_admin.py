from django.test import TestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from renthub.utils import Browser, kill_port, start_django_server, stop_django_server, admin_login


class AdminMaintenanceRequestDjangoTest(TestCase):

    def setUp(self):
        kill_port()
        self.server_process = start_django_server()
        self.browser = Browser.get_browser()

    def test_admin_can_view_maintenance_requests_in_admin_panel(self):
        # Step 1: Login
        admin_login(self.browser)

        # Step 2: Wait for Django admin panel and click on "Maintenance requests"
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Maintenance requests"))
        )
        self.browser.find_element(By.LINK_TEXT, "Maintenance requests").click()

        # Step 3: Wait until the request table is loaded
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@id='result_list']//tr[2]/th/a"))
        )

        # Now safely fetch the first maintenance request
        first_request = self.browser.find_element(By.XPATH, "//table[@id='result_list']//tr[2]/th/a").text
        title = self.browser.find_element(By.XPATH, "//table[@id='result_list']//tr[2]/td[1]").text
        message = self.browser.find_element(By.XPATH, "//table[@id='result_list']//tr[2]/td[2]").text

        print("First request rental:", first_request)
        print("Title:", title)
        print("Request Message:", message)

        self.assertIn("Room", first_request)
        self.assertTrue("test" in message.lower())

    def test_admin_can_approve_maintenance_request(self):
        # Step 1: Login
        admin_login(self.browser)

        # Step 2: Enter Maintenance requests section
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Maintenance requests"))
        )
        self.browser.find_element(By.LINK_TEXT, "Maintenance requests").click()

        # Step 3: Wait for table and open the first request
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@id='result_list']//tr[2]/th/a"))
        )
        self.browser.find_element(By.XPATH, "//table[@id='result_list']//tr[2]/th/a").click()

        # Step 4: Change status to 'approve'
        status_dropdown = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "status"))
        )
        Select(status_dropdown).select_by_visible_text("approve")

        # Step 5: Scroll to SAVE and click
        save_button = self.browser.find_element(By.NAME, "_save")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", save_button)
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.NAME, "_save")))
        save_button.click()

        # Step 6: Verify success message
        success_message = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".messagelist li"))
        )
        print("Success:", success_message.text)
        self.assertIn("changed successfully", success_message.text.lower())

    def test_admin_can_reject_maintenance_request(self):
        # Step 1: Login
        admin_login(self.browser)

        # Step 2: Go to Maintenance requests
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Maintenance requests"))
        )
        self.browser.find_element(By.LINK_TEXT, "Maintenance requests").click()

        # Step 3: Click first request in the list
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@id='result_list']//tr[2]/th/a"))
        )
        self.browser.find_element(By.XPATH, "//table[@id='result_list']//tr[2]/th/a").click()

        # Step 4: Change status to 'reject'
        status_dropdown = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "status"))
        )
        Select(status_dropdown).select_by_visible_text("reject")

        # Step 5: Scroll and click SAVE
        save_button = self.browser.find_element(By.NAME, "_save")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", save_button)
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.NAME, "_save")))
        save_button.click()

        # Step 6: Confirm success message
        success_message = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".messagelist li"))
        )
        print("Success:", success_message.text)
        self.assertIn("changed successfully", success_message.text.lower())

    def tearDown(self):
        stop_django_server(self.server_process)
        self.browser.quit()
        kill_port()
