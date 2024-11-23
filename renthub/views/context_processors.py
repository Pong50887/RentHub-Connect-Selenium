from ..models import Notification, Rental
from ..utils import Status


def unread_notifications_count(request):
    """ Provide the count of unread notifications for the authenticated user."""
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(renter=request.user, is_read=False).count()
        return {'unread_count': unread_count}
    return {'unread_count': 0}


def check_monthly_payment_due(_):
    rentals = Rental.objects.filter(status=Status.approve)
    for rental in rentals:
        rental.check_monthly_payment_due()

    return {}


def check_rental_ended(_):
    rentals = Rental.objects.filter(status=Status.approve)
    for rental in rentals:
        if rental.is_ended():
            rental.delete()

    return {}


def global_context(_):
    # Logic for contact details
    contact = {
        'location': '123 Main St, Bangkok, Thailand',
        'phone_number': '0987654321',
        'email': 'info@renthub.com'
    }

    return {'contact': contact}
