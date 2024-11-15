from django.db import models
from . import Rental, Renter
from ..utils import Status
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class RentalPayment(models.Model):
    room = models.ForeignKey("renthub.Room", on_delete=models.CASCADE)
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='slip_images/', blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices(),
        default=Status.wait,
    )


@receiver(post_save, sender=RentalPayment)
def update_rental_is_paid(sender, instance, **kwargs):
    rental = Rental.objects.get(room=instance.room, renter=instance.renter)
    rental.is_paid = True
    rental.last_paid_date = timezone.now().date()
    rental.save()
