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
    start_date = models.DateField('date rented', default=timezone.now)
    end_date = models.DateField('date checkout', null=True, blank=True)
    water_fee = models.IntegerField(default=0)
    electric_fee = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='slip_images/', blank=True, null=True)
    last_checked_month = models.DateField(null=True, blank=True)
    last_paid_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices(),
        default=Status.wait,
    )

    def is_ended(self):
        """Check if the event or rental period has ended."""
        if self.end_date:
            return timezone.now().date() > self.end_date

    def check_monthly_payment_due(self):
        """Check if a new month within the rental period requires payment."""
        now = timezone.now().date()
        if self.start_date <= now:

            months_elapsed = (now.year - self.start_date.year) * 12 + (now.month - self.start_date.month)

            if months_elapsed > 0:
                if self.last_checked_month != now.replace(day=1):
                    self.last_checked_month = now.replace(day=1)
                    self.last_paid_date = None
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

    def is_payment_on_time(self):
        """Checks if the last payment was made on time."""
        if self.start_date.year > timezone.now().year or (
                self.start_date.year == timezone.now().year and self.start_date.month >= timezone.now().month):
            return True

        if self.last_paid_date is None:
            return timezone.now().day <= 15

        return self.last_paid_date.day <= 15

    def check_overlapped(self):
        """
        Override save to ensure a room cannot have multiple active rentals.
        If a duplicate rental exists, delete the new one and notify the renter.
        """
        existing_rental = Rental.objects.filter(
            room=self.room,
        ).exclude(id=self.id).first()

        if existing_rental:
            Notification.objects.create(
                renter=self.renter,
                title="Rental Creation Failed",
                message=f"Your rental request for room {self.room} failed as it is already occupied. Contact admin.",
                post_date=timezone.now(),
                is_read=False
            )
        return existing_rental

    def __str__(self):
        """Returns the short detail of the request."""
        return f"{self.renter} / {self.room} / {self.status}"
