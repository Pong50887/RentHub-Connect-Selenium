from django.contrib import admin
from renthub.models import Transaction


class RentalAdmin(admin.ModelAdmin):
    list_display = ('room', 'renter', 'price', 'image_tag', 'status')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        return "No Image"

    image_tag.allow_tags = True
    image_tag.short_description = 'Payment Slip Image'

    def save_model(self, request, obj, form, change):

        super().save_model(request, obj, form, change)

        latest_transaction = Transaction.objects.filter(
            renter=obj.renter, room=obj.room
        ).order_by('-date').first()

        if latest_transaction:
            latest_transaction.status = obj.status
            latest_transaction.save()
