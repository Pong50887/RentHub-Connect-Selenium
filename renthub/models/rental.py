from django.utils import timezone
from django.db import models

from .room import Room
from .renter import Renter
from ..utils import Status


class Rental(models.Model):
    """
    Represents a rental agreement between a renter and a room.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    start_date = models.DateTimeField('date rented', default=timezone.now)
    end_date = models.DateTimeField('date checkout', default=timezone.now)
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
