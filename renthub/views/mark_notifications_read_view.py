from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Notification


class MarkNotificationsReadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        Notification.objects.filter(renter=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
