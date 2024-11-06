from django.contrib import admin


class AnnouncementAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing Announcement objects in the admin panel.
    """
    list_display = ('id', 'title', 'content', 'publish_date')
