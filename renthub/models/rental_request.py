from django.db import models

from .room import Room
from .renter import Renter


class RentalRequest(models.Model):
    """
    Represents a rental request for admin to check.
    """
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

