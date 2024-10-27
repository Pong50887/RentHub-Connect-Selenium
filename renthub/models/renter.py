from django.contrib.auth.models import User
from django.db import models


class Renter(User):
    """
    Represents a renter, extending Django's default User model.
    """
    phone_number = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Renter"
        verbose_name_plural = "Renters"

    def __str__(self):
        """Returns the username of the renter."""
        return self.username
