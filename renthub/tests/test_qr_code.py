import os
import django
from django.test import TestCase
from unittest.mock import patch, call, MagicMock
from ..utils import generate_qr_code, delete_qr_code

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()


class QRCodeUtilityTest(TestCase):
    """Test case for QR code generation and deletion."""

    def setUp(self):
        """Set up data for the tests."""
        self.room_number = "101"
        self.price = 7000.00
        self.qr_code_dir = "media/qr_code_images"
        self.qr_code_path = os.path.join(self.qr_code_dir, f"{self.room_number}.png")
        os.makedirs(self.qr_code_dir, exist_ok=True)
        self.mock_logger = patch('renthub.utils.logger').start()

    def tearDown(self):
        """Clean up any remaining QR code files after tests."""
        if os.path.exists(self.qr_code_path):
            os.remove(self.qr_code_path)
        try:
            os.rmdir(self.qr_code_dir)
        except OSError:
            pass
        patch.stopall()

    def test_generate_qr_code(self):
        """Test that the QR code is generated successfully."""
        generate_qr_code(self.price, self.room_number)
        self.mock_logger.info.assert_any_call(f"Generating QR code for room {self.room_number} with price {self.price}")
        self.mock_logger.info.assert_any_call(f"QR code generated successfully for room {self.room_number}.")
        self.assertTrue(os.path.exists(self.qr_code_path))

    def test_delete_qr_code(self):
        """Test that the QR code is deleted successfully."""
        with open(self.qr_code_path, 'w') as f:
            f.write("This is a mock QR code file.")
        self.assertTrue(os.path.exists(self.qr_code_path))

        with patch('renthub.utils.boto3.client') as mock_boto_client:
            mock_s3 = MagicMock()
            mock_boto_client.return_value = mock_s3

        delete_qr_code(self.room_number)
        self.assertFalse(os.path.exists(self.qr_code_path))

        self.mock_logger.info.assert_has_calls([
            call(f"QR code for room {self.room_number} deleted successfully."),
            call(f"QR code for room {self.room_number} deleted from S3 successfully.")])
