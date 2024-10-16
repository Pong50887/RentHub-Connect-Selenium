from django.db import models

from .room_type import RoomType


class Feature(models.Model):
    room_type = models.ForeignKey(RoomType, related_name='features', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
