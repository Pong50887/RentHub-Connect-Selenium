from django.contrib import admin
from renthub.models import Transaction, Rental, Notification


class RentalAdmin(admin.ModelAdmin):
    list_display = ('room', 'renter', 'price', 'image_tag', 'status', 'is_paid', 'last_checked_month')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        return "No Image"

    image_tag.allow_tags = True
    image_tag.short_description = 'Payment Slip Image'

    def save_model(self, request, obj, form, change):

        original_status = None
        if change:
            original_status = Rental.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if obj.status == "approve" and original_status != "approve":
            self.create_notification(obj.renter, "Rental Approved", f"Your rental for {obj.room} has been approved.")

        elif obj.status == "reject" and original_status != "reject":
            self.create_notification(obj.renter, "Rental Rejected", f"Your rental for {obj.room} has been rejected.")
            obj.delete()

        latest_transaction = Transaction.objects.filter(
            renter=obj.renter, room=obj.room
        ).order_by('-date').first()

        if latest_transaction:
            latest_transaction.status = obj.status
            latest_transaction.save()

    def create_notification(self, renter, title, message):
        """Create a new notification for the renter."""
        Notification.objects.create(renter=renter, title=title, message=message)
