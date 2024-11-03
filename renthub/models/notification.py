from django.db import models
from .renter import Renter


class Notification(models.Model):
    """
    Represents a notification for a renter.
    """
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-post_date']
