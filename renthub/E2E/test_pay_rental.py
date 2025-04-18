from django.test import TestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

from renthub.utils import kill_port, Browser, start_django_server, log_in, stop_django_server


class PaymentFlowTest(TestCase):

    def setUp(self):
        kill_port()
        self.browser = Browser.get_browser()
        self.server_process = start_django_server()

    def test_user_can_submit_rental_payment(self):
        # Step 1: Login
        log_in(driver=self.browser, username="demo1", password="hackme11")

        # Step 2: Click "My Rentals"
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "My Rentals"))
        ).click()

        # Step 3: Click "Pay Rental" button
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Pay Rental')]"))
        )

        pay_button = self.browser.find_element(By.XPATH, "//a[contains(text(), 'Pay Rental')]")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", pay_button)
        pay_button.click()

        # Step 4: Upload payment slip
        upload_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "payment_slip"))
        )

        # Scroll into view before uploading
        self.browser.execute_script("arguments[0].scrollIntoView(true);", upload_input)

        # Absolute path for the image
        slip_path = os.path.abspath("renthub/E2E/test_assets/example_image.png")
        upload_input.send_keys(slip_path)

        # Step 5: Click Send
        send_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
        self.browser.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", send_button)
        WebDriverWait(self.browser, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send')]")))
        self.browser.execute_script("arguments[0].click();", send_button)  # Use JS to avoid visual overlap

        # Step 6: Assert success message on homepage
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.alert"))
        )
        success_message = self.browser.find_element(By.XPATH, "//ul[contains(@class, 'alert')]/li").text
        print("Payment Success:", success_message)
        self.assertIn("your rental request was submitted successfully", success_message.lower())

    def test_payment_button_disappears_after_submit(self):

        # Step 1: Login
        log_in(driver=self.browser, username="demo2", password="hackme22")

        # Step 2: Click "My Rentals" (wait + locate + click separately)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "My Rentals"))
        )
        self.browser.find_element(By.LINK_TEXT, "My Rentals").click()

        # Step 3: Wait for the button and verify it says "View Details"
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "view-detail-btn"))
        )
        button_text = self.browser.find_element(By.CLASS_NAME, "view-detail-btn").text
        print("Button text after payment:", button_text)
        self.assertIn("view details", button_text.lower())

    # def test_user_cannot_submit_without_slip(self):
    #     log_in(driver=self.browser, username="demo1", password="hackme11")
    #
    #     # Step 1: Go to My Rentals
    #     WebDriverWait(self.browser, 10).until(
    #         EC.presence_of_element_located((By.LINK_TEXT, "My Rentals"))
    #     ).click()
    #
    #     # Step 2: Click "Pay Rental"
    #     WebDriverWait(self.browser, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Pay Rental')]"))
    #     ).click()
    #
    #     # Step 3: Scroll and try to submit without selecting a file
    #     send_button = WebDriverWait(self.browser, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Send')]"))
    #     )
    #     self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", send_button)
    #     WebDriverWait(self.browser, 2).until(
    #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send')]")))
    #     self.browser.execute_script("arguments[0].click();", send_button)
    #
    #     # Step 4: Verify the alert message appears
    #     alert_message = WebDriverWait(self.browser, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'alert')]/li"))
    #     ).text
    #     print("Validation Message:", alert_message)
    #     self.assertIn("no payment slip uploaded", alert_message.lower())

    def test_user_can_view_payment_history(self):
        # Step 1: Login
        log_in(driver=self.browser, username="demo4", password="hackme44")

        # Step 2: Go to My Rentals
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "My Rentals"))
        ).click()

        # Step 3: Scroll to 'Rental History' heading
        rental_history_heading = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Rental History')]"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})",
                                    rental_history_heading)

        # Step 4: Wait for View Details buttons (indicate transactions)
        view_buttons = WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'View Details')]"))
        )
        self.assertGreater(len(view_buttons), 0, "Expected at least one 'View Details' button under Rental History.")

    def test_user_can_revisit_rental_payment_detail(self):
        # Step 1: Login
        log_in(driver=self.browser, username="demo4", password="hackme44")

        # Step 2: Go to My Rentals
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "My Rentals"))
        ).click()

        # Step 3: Scroll to bottom (rental history section)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Step 4: Wait for and find the View Details button under Rental History
        rental_history = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Rental History')]"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView(true);", rental_history)

        # Narrow down to View Details that appears after Rental History
        view_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "(//*[contains(text(), 'Rental History')]/following::a[contains(text(), 'View Details')])[1]"))
        )
        self.browser.execute_script("arguments[0].click();", view_button)

        # Step 5: Assert Payment Details is visible
        payment_heading = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Payment Details')]"))
        )
        self.assertIn("Payment Details", payment_heading.text)

        room_number = self.browser.find_element(By.XPATH, "//h5[contains(text(), 'Room Number')]").text
        self.assertIn("Room Number", room_number)

    def tearDown(self):
        stop_django_server(self.server_process)
        self.browser.quit()
        kill_port()
