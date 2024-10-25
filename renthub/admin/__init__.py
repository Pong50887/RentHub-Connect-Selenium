from django.contrib import admin
from ..models import Room, RoomType, Announcement, Rental, Notification, Transaction

from .feature_in_line import FeatureInline
from .room_admin import RoomAdmin
from .room_type_admin import RoomTypeAdmin
from .announcement_admin import AnnouncementAdmin
from .announcement_form import AnnouncementForm
from .notification_admin import NotificationAdmin
from .rental_admin import RentalAdmin
from .transaction_admin import TransactionAdmin

admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Rental, RentalAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Transaction, TransactionAdmin)
