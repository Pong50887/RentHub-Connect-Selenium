from django.views.generic import DetailView

from ..models import Announcement


class AnnouncementView(DetailView):
    """
    View for displaying the details of a specific announcement.
    """
    model = Announcement
    template_name = "renthub/announcement.html"
