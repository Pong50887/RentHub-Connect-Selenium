from django.contrib import admin


class MaintenanceRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for the MaintenanceRequest model.
    """
    list_display = ('rental', 'request_message', 'date_requested', 'status')
