from django.contrib import admin

from ..models import Room, RoomType, Announcement

from .feature_in_line import FeatureInline
from .room_admin import RoomAdmin
from .room_type_admin import RoomTypeAdmin
from .announcement_admin import AnnouncementAdmin
from .announcement_form import AnnouncementForm

admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
