from django.contrib import admin


class PropertyOwnerAdmin(admin.ModelAdmin):
    """
    Admin interface for managing PropertyOwner records.
    """
    list_display = ('username', 'email', 'phone_number', 'location')
    fields = ['username', 'password', 'email', 'phone_number', 'location']
