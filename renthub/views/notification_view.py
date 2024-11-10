from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Notification


class NotificationView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'renthub/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(renter=self.request.user).order_by('-post_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_notifications'] = Notification.objects.filter(
            renter=self.request.user, is_read=False
        ).order_by('-post_date')
        return context
