from django.contrib import admin


class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'detail', 'price', 'availability', 'room_type')
