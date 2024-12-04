from django.contrib import admin

from renthub.models import Notification, Renter


class RenterAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Renter model.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'thai_citizenship_id',
                    'thai_citizenship_id_image', 'is_valid')

    def save_model(self, request, obj, form, change):
        original_status = None
        if change:
            original_status = Renter.objects.get(pk=obj.pk).is_valid

        super().save_model(request, obj, form, change)

        if obj.is_valid is True and original_status is not True:
            self.create_notification(obj, "Your identity has been Approved", f"Your identity information has been "
                                                                             f"verified successfully.")

        elif obj.is_valid is False and original_status is not False:
            self.create_notification(obj, "Your identity is Invalid", f"Your identity information is invalid, "
                                                                      f"please submit a new citizenship ID image.")

    @staticmethod
    def create_notification(renter, title, message):
        """Create a new notification for the renter."""
        Notification.objects.create(renter=renter, title=title, message=message)
