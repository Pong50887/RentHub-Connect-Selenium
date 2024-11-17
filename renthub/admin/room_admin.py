from django.contrib import admin


class RoomAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Room model.
    """
    list_display = ('room_number', 'room_floor', 'detail', 'price', 'room_type')
