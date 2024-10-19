from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Notification

class NotificationView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'renthub/notifications.html'
    context_object_name = 'notifications'
    ordering = ['-post_date']

    def get_queryset(self):
        return Notification.objects.filter(renter=self.request.user)
