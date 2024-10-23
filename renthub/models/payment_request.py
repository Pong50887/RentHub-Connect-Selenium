from django.db import models

from .room import Room

class PaymentRequest(models.Model):
    """
    Represents a payment request for user to receive.
    """
    title = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    detail = models.CharField(blank=True, null=True)
    end_date = models.DateTimeField('end date', null=True, blank=True)
