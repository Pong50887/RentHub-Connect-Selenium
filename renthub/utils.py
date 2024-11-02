from promptpay import qrcode
import os
import logging
from enum import Enum

from django.conf import settings
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger('renthub')
s3_client = boto3.client('s3')
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
