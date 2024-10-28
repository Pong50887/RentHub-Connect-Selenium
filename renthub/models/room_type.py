from django.db import models


class RoomType(models.Model):
    """
    Represents a type of room with a shared image for each type.
    """
    type_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    ideal_for = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        """Returns the name of the room type."""
        return self.type_name
