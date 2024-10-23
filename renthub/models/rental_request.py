from django.db import models

from .room import Room
from .renter import Renter
from ..utils import Status


class RentalRequest(models.Model):
    """
    Represents a rental request for admin to check.
    """
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='slip_images/', blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices(),
        default=Status.wait,
    )

    def __str__(self):
        """Returns the short detail of the request."""
        return f"{self.renter} / {self.room} / {self.status}"
