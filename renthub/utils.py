import logging
import os
import signal
import subprocess
import time
from enum import Enum

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.urls import reverse
from promptpay import qrcode
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from mysite import settings
from renthub.models import RoomType

logger = logging.getLogger('renthub')


def get_s3_client():
    """Get S3 client for authentication to access S3 storage."""
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )


s3_client = get_s3_client()
BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME


def generate_qr_code(price, room_number):
    """Generate Promptpay QR payment with fixed price."""
    try:
        logger.info(f"Generating QR code for room {room_number} with price {price}")
        payload_with_amount = qrcode.generate_payload("0983923856", price)
        qr_code_path = f"media/qr_code_images/{room_number}.png"
        qrcode.to_file(payload_with_amount, qr_code_path)
        logger.info(f"QR code generated successfully for room {room_number}.")

        s3_client.upload_file(qr_code_path, BUCKET_NAME, f"qr_code_images/{room_number}.png")
        logger.info(f"QR code generated and uploaded successfully for room {room_number}.")
    except ClientError as e:
        logger.error(f"Failed to upload QR code to S3: {e}")
    except Exception as e:
        logger.error(f"Failed to generate QR code: {e}")


def delete_qr_code(room_number):
    """Delete the QR code file for a specific room after receipt submission."""
    qr_code_path = f"media/qr_code_images/{room_number}.png"

    if os.path.exists(qr_code_path):
        os.remove(qr_code_path)
        logger.info(f"QR code for room {room_number} deleted successfully.")
    else:
        logger.debug(f"QR code for room {room_number} not found.")

    s3_key = f"qr_code_images/{room_number}.png"
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
        logger.info(f"QR code for room {room_number} deleted from S3 successfully.")
    except ClientError as e:
        logger.error(f"Failed to delete QR code from S3: {e}")


class Status(Enum):
    """Status Enum to ensure a consistant status value across all implementation throughout the project."""

    approve = 'approve'
    reject = 'reject'
    wait = 'wait'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        """Returns the choices as a list of tuples."""
        return [(status.name, status.value) for status in cls]


def get_rental_progress_data(status):
    """Return milestones information regarding rental request approval status."""
    milestones = [
        {"step": 1, "description": "Payment Slip", "status": "Pending", "symbol": ""},
        {"step": 2, "description": "Rent Approval", "status": "Pending", "symbol": ""},
    ]

    if status == str(Status.wait):
        milestones[0]["status"] = "Submitted"
        milestones[0]["symbol"] = "o"
    elif status == str(Status.approve):
        milestones[0]["status"] = "Submitted"
        milestones[0]["symbol"] = "o"

        milestones[1]["status"] = "Approved"
        milestones[1]["symbol"] = "o"

    elif status == str(Status.reject):
        milestones[0]["status"] = "Submitted"
        milestones[0]["symbol"] = "o"

        milestones[1]["status"] = "Rejected"
        milestones[1]["symbol"] = "x"

    return milestones


def get_room_images(room_type: RoomType):
    """Return list of room type's image urls"""
    image_url_list = []
    image_folder_path = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/room_images/{room_type.id}/'
    image_url_list.append(f"{image_folder_path}bedroom.jpg")
    image_url_list.append(f"{image_folder_path}bathroom.jpg")
    image_url_list.append(f"{image_folder_path}kitchen.jpg")
    return image_url_list


class Browser:
    """Provide access to an instance of a Selenium web driver."""

    @classmethod
    def get_browser(cls):
        """Class method to initialize a headless Chrome WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver

    @classmethod
    def start_django_server(cls):
        """Start the Django server using the test database."""
        server_command = ['python3', 'manage.py', 'runserver', '127.0.0.1:8000']
        cls.server_process = subprocess.Popen(server_command)
        time.sleep(5)

    @classmethod
    def stop_django_server(cls):
        """Stop the Django development server."""
        cls.server_process.terminate()

    @classmethod
    def get_logged_in_browser(cls, username, password):
        """Class method to initialize a headless browser and log in."""
        driver = cls.get_browser()

        try:
            driver.get(f"{settings.BASE_URL}/accounts/login/?next=/")
            username_field = driver.find_element(By.XPATH, '//td//input[@name="username"]')
            password_field = driver.find_element(By.XPATH, '//td//input[@name="password"]')
            login_button = driver.find_element(By.XPATH, '//form//button[@type="submit"]')

            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.click()

            WebDriverWait(driver, 10).until(EC.url_to_be(f"{settings.BASE_URL}{reverse('renthub:home')}"))

        except Exception as e:
            raise RuntimeError(f"An error occurred during login: {e}")

        return driver


def kill_port():
    # Specify the port to check
    port = 8000

    try:
        # Find the process using the port
        result = subprocess.run(
            ["lsof", "-i", f":{port}"], capture_output=True, text=True
        )
        lines = result.stdout.splitlines()

        # Parse the output to get the PID (Process ID)
        if len(lines) > 1:  # First line is the header, skip it
            pid = int(lines[1].split()[1])  # Extract PID from the output
            print(f"Terminating process on port {port} with PID {pid}")

            # Kill the process
            os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(f"Failed to free port {port}: {e}")


def admin_login(browser):
    browser.get(f"{settings.BASE_URL}/admin/login/")
    browser.find_element(By.NAME, 'username').send_keys('rhadmin')
    browser.find_element(By.NAME, 'password').send_keys('renthub1234')
    browser.find_element(By.XPATH, '//input[@type="submit"]').click()
