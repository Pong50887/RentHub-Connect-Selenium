from django.contrib import admin
from .models import Room, RoomType, Feature


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1  # Number of empty forms shown by default


class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'detail', 'price', 'availability', 'room_type')


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


admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
