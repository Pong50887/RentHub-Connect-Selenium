from django.db import models

from .room import Room
from .renter import Renter


class Transaction(models.Model):
    """
    Represents a transaction related to a rental.
    """
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    image = models.ImageField(upload_to='slip_images/', blank=True, null=True)
