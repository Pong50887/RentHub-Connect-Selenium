from django.contrib.auth.models import User
from django.db import models


class Renter(User):
    """
    Represents a renter, extending Django's default User model.
    """
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.username
