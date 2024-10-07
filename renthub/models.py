from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('wait', 'Wait'),
]


class Room(models.Model):
    """
    Represents a room available for rent.
    """
    room_number = models.IntegerField(default=0)
    detail = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=200)
    availability = models.BooleanField()

    def __str__(self):
        """Returns the string representation of the room, which is its detail."""
        return self.detail


class Renter(User):
    """
    Represents a renter, extending Django's default User model.
    """
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return User.username


class Rental(models.Model):
    """
    Represents a rental agreement between a renter and a room.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    start_data = models.DateTimeField('date rented', default=timezone.now)
    end_date = models.DateTimeField('date checkout', default=timezone.now)
    rental_fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='wait',
    )


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

    def str(self):
        """Returns the string representation of the transaction, which is its status."""
        return self.status


class MaintenanceRequest(models.Model):
    """
    Represents a maintenance request made by a renter.
    """
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    request_message = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='wait',
    )
    date_requested = models.DateTimeField()

    def str(self):
        """Returns a string representation of the maintenance request."""
        return f'Request by {self.rental.renter} for {self.rental.room}'


class Announcement(models.Model):
    """
    Represents an announcement for the tenants.
    """
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=500)
    publish_date = models.DateTimeField()

    def str(self):
        """Returns the string representation of the announcement, which is its title."""
        return self.title
