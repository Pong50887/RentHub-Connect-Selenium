from django.db import models

from .rental import Rental

STATUS_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('wait', 'Wait'),
]


class Transaction(models.Model):
    """
    Represents a transaction related to a rental.
    """
    detail = models.CharField(max_length=255)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='wait',
    )

    def __str__(self):
        """Returns the string representation of the transaction, which is its status."""
        return self.status
