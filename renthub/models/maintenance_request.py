from django.db import models

from .rental import Rental

STATUS_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('wait', 'Wait'),
]


class MaintenanceRequest(models.Model):
    """
    Represents a maintenance request made by a renter.
    """
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    request_message = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='wait',
    )
    date_requested = models.DateTimeField()

    def __str__(self):
        """Returns a string representation of the maintenance request."""
        return f'Request by {self.rental.renter} for {self.rental.room}'
