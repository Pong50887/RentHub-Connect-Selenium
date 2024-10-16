from django.db import models

from .room_type import RoomType


class Room(models.Model):
    """
    Represents a room available for rent.
    """
    room_number = models.IntegerField(default=0)
    detail = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """Returns the string representation of the room, which is its detail."""
        return str(self.room_number)
