from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Notification


class MarkNotificationsReadView(LoginRequiredMixin, View):
    """A view to mark all unread notifications as read for the authenticated user."""

    def post(self, request, *args, **kwargs):
        """Mark the Notification as read."""
        Notification.objects.filter(renter=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
