from ..models import Notification, Rental


def unread_notifications_count(request):
    """ Provide the count of unread notifications for the authenticated user."""
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(renter=request.user, is_read=False).count()
        return {'unread_count': unread_count}
    return {'unread_count': 0}


def check_monthly_payment_due(request):
    if request.user.is_authenticated:
        rentals = Rental.objects.filter(renter=request.user)
        for rental in rentals:
            rental.check_monthly_payment_due()

    return {}
