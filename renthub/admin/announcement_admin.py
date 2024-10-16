from django.contrib import admin

from .announcement_form import AnnouncementForm


class AnnouncementAdmin(admin.ModelAdmin):
    form = AnnouncementForm
    list_display = ('id', 'title', 'content', 'publish_date')
