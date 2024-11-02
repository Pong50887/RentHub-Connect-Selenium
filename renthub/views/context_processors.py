from ..models import Notification


def unread_notifications_count(request):
    """ Provide the count of unread notifications for the authenticated user."""
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(renter=request.user, is_read=False).count()
        return {'unread_count': unread_count}
    return {'unread_count': 0}
