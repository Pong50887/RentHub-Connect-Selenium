from django.db import models

from .room_type import RoomType


class Feature(models.Model):
    """
    Represents a feature associated with a specific RoomType.
    """
    room_type = models.ForeignKey(RoomType, related_name='features', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        """Returns a string representation of the Feature, specifically its name."""
        return self.name
