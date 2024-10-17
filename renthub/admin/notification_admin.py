from django.contrib import admin
from ..models import Notification, Renter

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['renter', 'title', 'post_date', 'is_read']
    list_filter = ['renter', 'is_read']
