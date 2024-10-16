from django.views.generic import DetailView

from ..models import Announcement


class AnnouncementView(DetailView):
    model = Announcement
    template_name = "renthub/announcement.html"
