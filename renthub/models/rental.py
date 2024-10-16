from django.utils import timezone
from django.db import models

from .room import Room
from .renter import Renter

STATUS_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('wait', 'Wait'),
]


class Rental(models.Model):
    """
    Represents a rental agreement between a renter and a room.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    start_date = models.DateTimeField('date rented', default=timezone.now)
    end_date = models.DateTimeField('date checkout', default=timezone.now)
    rental_fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='wait',
    )
