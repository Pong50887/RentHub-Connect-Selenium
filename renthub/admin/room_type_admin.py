from django.contrib import admin

from .feature_in_line import FeatureInline


class RoomTypeAdmin(admin.ModelAdmin):
    inlines = [FeatureInline]
    list_display = ('type_name', 'description', 'ideal_for', 'image_tag',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        return "No Image"

    image_tag.allow_tags = True
    image_tag.short_description = 'Room Type Image'
