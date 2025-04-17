import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class UnauthorizedAccessTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def test_unauthenticated_access_to_admin_redirects_to_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/admin/")

        # Wait for the login form to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        current_url = driver.current_url
        print("Redirected to:", current_url)

        self.assertIn("/admin/login", current_url)
        self.assertIn("username", driver.page_source.lower())
        self.assertIn("password", driver.page_source.lower())

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
