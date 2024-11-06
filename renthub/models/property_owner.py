from django.contrib.auth.models import User
from django.db import models


class PropertyOwner(User):
    """
    Represents the contact information for the organization,
    """
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    is_superuser = True

    class Meta:
        verbose_name = "Property Owner"

    def __str__(self):
        """Returns a string representation of the contact information."""
        return f"Username: {self.username}, Phone: {self.phone_number}"
