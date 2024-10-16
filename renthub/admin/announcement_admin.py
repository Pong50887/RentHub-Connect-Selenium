from django.contrib import admin

from .announcement_form import AnnouncementForm


class AnnouncementAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing Announcement objects in the admin panel.
    """
    form = AnnouncementForm
    list_display = ('id', 'title', 'content', 'publish_date')
