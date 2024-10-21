from django.contrib import admin


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('renter', 'room', 'price', 'date', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        return "No Image"

    image_tag.allow_tags = True
    image_tag.short_description = 'Payment Slip Image'
