from django.contrib import admin
from ..models import Room, RoomType, Announcement, Renter, Rental, Notification, Transaction, MaintenanceRequest, \
    Feature, PropertyOwner, RentalPayment

from .feature_in_line import FeatureInline
from .room_admin import RoomAdmin
from .room_type_admin import RoomTypeAdmin
from .announcement_admin import AnnouncementAdmin
from .notification_admin import NotificationAdmin
from .rental_admin import RentalAdmin
from .transaction_admin import TransactionAdmin
from .renter_admin import RenterAdmin
from .maintenance_request_admin import MaintenanceRequestAdmin
from .maintenance_request_form import MaintenanceRequestForm
from .feature_admin import FeatureAdmin
from .property_owner_admin import PropertyOwnerAdmin
from.rental_payment_admin import RentalPaymentAdmin

admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Rental, RentalAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Renter, RenterAdmin)
admin.site.register(MaintenanceRequest, MaintenanceRequestAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(PropertyOwner, PropertyOwnerAdmin)
admin.site.register(RentalPayment, RentalPaymentAdmin)
