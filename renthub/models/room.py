from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
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

    def is_available(self, start_date, number_month):
        """
        Checks if the room is available between the given start and end dates.
        """
        start_date = datetime.strptime(start_date, "%Y-%m").date()
        end_time = start_date + relativedelta(months=number_month)
        overlapping_rentals = Rental.objects.filter(
            room=self,
            start_date__lt=end_time,
            end_date__gt=start_date,
            status__in=[Status.wait, Status.approve]
        )
        return not overlapping_rentals.exists()

    def __str__(self):
        """Returns the string representation of the room, which includes its room number and details."""
        return f"Room {self.room_number} - {self.detail}"
