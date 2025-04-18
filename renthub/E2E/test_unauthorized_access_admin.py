from django.test import TestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mysite import settings
from renthub.utils import Browser, kill_port, start_django_server, stop_django_server


class UnauthorizedAccessTests(TestCase):

    def setUp(self):
        kill_port()
        self.server_process = start_django_server()
        self.browser = Browser.get_browser()

    def test_unauthenticated_access_to_admin_redirects_to_login(self):
        self.browser.get(f"{settings.BASE_URL}/admin")

        # Wait for the login form to appear
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        current_url = self.browser.current_url
        print("Redirected to:", current_url)

        self.assertIn("/admin/login", current_url)
        self.assertIn("username", self.browser.page_source.lower())
        self.assertIn("password", self.browser.page_source.lower())

    def tearDown(self):
        stop_django_server(self.server_process)
        self.browser.quit()
        kill_port()