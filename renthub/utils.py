from promptpay import qrcode
import os
import logging

logger = logging.getLogger('renthub')


def generate_qr_code(price, room_number):
    """Generate Promptpay QR payment with fixed price."""
    try:
        logger.info(f"Generating QR code for room {room_number} with price {price}")
        payload_with_amount = qrcode.generate_payload("0983923856", price)
        qrcode.to_file(payload_with_amount, f"media/qr_code_images/{room_number}.png")
        logger.info(f"QR code generated successfully for room {room_number}.")
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
