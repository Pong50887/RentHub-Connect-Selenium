from django.contrib import admin


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('renter', 'room', 'price', 'date', 'image_tag', 'renter_is_valid')
    readonly_fields = ('image_tag', 'renter_is_valid')

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        return "No Image"

    image_tag.allow_tags = True
    image_tag.short_description = 'Payment Slip Image'

    def renter_is_valid(self, obj):
        """Display the is_valid attribute from the associated renter."""
        return obj.renter.is_valid if obj.renter else False

    renter_is_valid.boolean = True
    renter_is_valid.short_description = "Renter Validity"