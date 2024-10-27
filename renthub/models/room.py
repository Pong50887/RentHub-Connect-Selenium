from datetime import timedelta

from django.db import models
from django.utils import timezone
from .room_type import RoomType
from .rental import Rental
from ..utils import Status


class Room(models.Model):
    """
    Represents a room available for rent.
    """
    room_number = models.IntegerField(default=0)
    detail = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True, blank=True)

    def is_available(self):
        """
        Checks if the room is available between the given start and end dates.
        """
        overlapping_rentals = Rental.objects.filter(
            room=self,
            start_date__lt=timezone.now() + timedelta(days=30),
            end_date__gt=timezone.now(),
            status__in=[Status.wait, Status.approve]
        )
        return not overlapping_rentals.exists()

    def __str__(self):
        """Returns the string representation of the room, which includes its room number and details."""
        return f"Room {self.room_number} - {self.detail}"
