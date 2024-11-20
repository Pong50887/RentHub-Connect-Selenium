from django.contrib import admin

from ..models import RoomImage


class RoomImageInline(admin.TabularInline):
    """
    Inline admin configuration for RoomImage.
    """
    model = RoomImage
    fields = ['image']
    extra = 1