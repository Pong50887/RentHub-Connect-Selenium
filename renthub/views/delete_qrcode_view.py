from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from renthub.utils import delete_qr_code, logger


class DeleteQRCodeView(LoginRequiredMixin, View):
    """View to delete the QR code for a specific room."""

    def post(self, request, room_number):
        """Delete the QR code for the specified room."""
        try:
            delete_qr_code(room_number)
            return JsonResponse({'success': True})
        except Exception as e:
            logger.error(f"Error deleting QR code for room {room_number}: {e}")
            return JsonResponse({'success': False}, status=500)
