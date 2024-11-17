from django.contrib import admin

from ..forms import MaintenanceRequestForm


class MaintenanceRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for the MaintenanceRequest model.
    """
    form = MaintenanceRequestForm
    list_display = ('rental', 'title', 'request_message', 'status', 'date_requested')
    fields = ['title', 'request_message', 'status']
