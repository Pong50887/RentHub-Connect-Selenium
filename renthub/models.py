from django.db import models


class Room(models.Model):
    detail = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=200)
    availability = models.BooleanField()

    def __str__(self):
        return self.detail

