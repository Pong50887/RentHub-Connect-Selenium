from django.db import models
from .room import Room

def upload_to_room_directory(instance, filename):
    # Access the related room's id from the instance
    return f'room_images/{instance.room.room_number}/{filename}'

class RoomImage(models.Model):
    """
    Represents a room image associated with a specific Room.
    """
    room = models.ForeignKey(Room, related_name='room_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_room_directory, blank=True, null=True)

    def __str__(self):
        """Returns a string representation of the image, specifically its name."""
        return self.image.url
