from datetime import timedelta

from django.utils import timezone
from django.db import models
from .renter import Renter
from ..utils import Status
from .notification import Notification


class Rental(models.Model):
    """
    Represents a rental agreement between a renter and a room.
    """
    room = models.ForeignKey("renthub.Room", on_delete=models.CASCADE)
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    start_date = models.DateTimeField('date rented', default=timezone.now)
    end_date = models.DateTimeField('date checkout', default=timezone.now() + timedelta(days=30))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='slip_images/', blank=True, null=True)
    last_checked_month = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices(),
        default=Status.wait,
    )

    def is_ended(self):
        """Check if the event or rental period has ended."""
        return timezone.now() > self.end_date

    def check_monthly_payment_due(self):
        """Check if a new month within the rental period requires payment."""
        now = timezone.now()
        if self.start_date <= now < self.end_date:

            months_elapsed = (now.year - self.start_date.year) * 12 + (now.month - self.start_date.month)

            if months_elapsed > 0:
                if self.last_checked_month != now.date().replace(day=1):
                    self.last_checked_month = now.date().replace(day=1)
                    self.is_paid = False
                    self.create_payment_notification()
                    self.save()

    def create_payment_notification(self):
        """Create a notification for the renter when payment is due."""

        Notification.objects.create(
            renter=self.renter,
            title="Payment Due",
            message=f"Your payment for the rental of {self.room} is due for this month.",
            post_date=timezone.now(),
            is_read=False
        )

    def __str__(self):
        """Returns the short detail of the request."""
        return f"{self.renter} / {self.room} / {self.status}"
