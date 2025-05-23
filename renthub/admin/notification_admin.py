from django.contrib import admin


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['renter', 'title', 'post_date', 'is_read']
    list_filter = ['renter', 'is_read']
