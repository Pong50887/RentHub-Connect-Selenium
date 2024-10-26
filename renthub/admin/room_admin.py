from django.contrib import admin


class RoomAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Room model.
    """
    list_display = ('room_number', 'detail', 'price', 'is_available', 'room_type')
