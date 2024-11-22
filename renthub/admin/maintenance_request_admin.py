from django.contrib import admin

from ..forms import MaintenanceRequestForm
from ..models import Notification, MaintenanceRequest


class MaintenanceRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for the MaintenanceRequest model.
    """
    form = MaintenanceRequestForm
    list_display = ('rental', 'title', 'request_message', 'status', 'date_requested')
    fields = ['rental', 'title', 'request_message', 'status']

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to send a notification when the status is changed to 'approve'.
        """
        original_status = None
        if change:
            original_status = MaintenanceRequest.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if obj.status == "approve" and original_status != "approve":
            self.create_notification(
                obj.rental.renter,
                "Maintenance Request Approved",
                f"Your maintenance request for {obj.rental.room} has been approved."
            )

    @staticmethod
    def create_notification(renter, title, message):
        """Create a new notification for the renter."""
        Notification.objects.create(renter=renter, title=title, message=message)
