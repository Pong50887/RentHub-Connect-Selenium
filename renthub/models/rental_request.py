from django.db import models, transaction
from django.utils import timezone

from .room import Room
from .renter import Renter
from .rental import Rental
from ..utils import Status


class RentalRequest(models.Model):
    """
    Represents a rental request for admin to check.
    """
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='slip_images/', blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices(),
        default=Status.wait,
    )

    def __str__(self):
        """Returns the short detail of the request."""
        return f"{self.renter} / {self.room} / {self.status}"

    @transaction.atomic
    def verify_rental(self, approved=True, end_date=None):
        """
        Admin verifies the rental request.

        If approved, creates a Rental and updates status to 'approved'.
        If rejected, updates status to 'rejected'.
        Both cases delete the rental request.
        """
        if approved:
            # Create the Rental object using request data
            Rental.objects.create(
                renter=self.renter,
                room=self.room,
                start_date=timezone.now(),
                end_date=end_date or timezone.now(),  # Use provided or current date
                rental_fee=self.price,
            )
            self.status = Status.approve
        else:
            self.status = Status.reject

        # Save the updated status and delete the rental request
        self.save()
        self.delete()

        # Return the updated status for logging or further processing
        return self.status
