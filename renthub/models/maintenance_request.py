from django.db import models

from .rental import Rental
from ..utils import Status


class MaintenanceRequest(models.Model):
    """
    Represents a maintenance request made by a renter.
    """
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    request_message = models.TextField()
    title = models.CharField(max_length=100, null=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices(),
        default=Status.wait,
    )
    date_requested = models.DateTimeField()

    def __str__(self):
        """Returns a string representation of the maintenance request."""
        return f'Request by {self.rental.renter} for {self.rental.room}'
