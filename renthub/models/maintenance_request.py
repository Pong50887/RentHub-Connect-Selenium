from django.db import models

from .rental import Rental
from ..utils import Status


class MaintenanceRequest(models.Model):
    """
    Represents a maintenance request made by a renter.
    """
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    request_message = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices(),
        default=Status.WAIT,
    )
    date_requested = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Override save to normalize the status to lowercase."""
        self.status = self.status.title()
        super().save(*args, **kwargs)

    def __str__(self):
        """Returns a string representation of the maintenance request."""
        return f'Request by {self.rental.renter} for {self.rental.room}'
