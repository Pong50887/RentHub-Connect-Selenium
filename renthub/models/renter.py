from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


def upload_to_renter_citizenship_directory(instance, filename):
    return f'renters/{instance.username}/{filename}'


class Renter(User):
    """
    Represents a renter, extending Django's default User model.
    """
    phone_number = models.CharField(max_length=10,
                                    validators=[
                                        RegexValidator(
                                            regex=r'^\d+$',
                                            message="Phone number can only contain numbers."
                                        )
                                    ])
    thai_citizenship_id = models.CharField(max_length=13,
                                           validators=[
                                               RegexValidator(
                                                   regex=r'^\d+$',
                                                   message="Citizenship ID can only contain numbers."
                                               )
                                           ], blank=True, null=True, unique=True)
    thai_citizenship_id_image = models.ImageField(upload_to=upload_to_renter_citizenship_directory, blank=True,
                                                  null=True)
    is_valid = models.BooleanField(
        default=False,
        help_text="Is the renter's thai_citizenship_id_image valid?"
    )

    class Meta:
        verbose_name = "Renter"
        verbose_name_plural = "Renters"

    def __str__(self):
        """Returns the username of the renter."""
        return self.username
