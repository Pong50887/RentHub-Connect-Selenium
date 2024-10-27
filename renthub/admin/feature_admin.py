from django.contrib import admin


class FeatureAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Feature model.
    """
    list_display = ('room_type', 'name')
