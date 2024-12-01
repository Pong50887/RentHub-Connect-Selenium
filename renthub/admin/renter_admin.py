from django.contrib import admin


class RenterAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Renter model.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'thai_citizenship_id',
                    'thai_citizenship_id_image')
