from django.views.generic import ListView

from ..models import RoomType, Announcement


class HomeView(ListView):
    """
    View for displaying the home page with a list of available room types
    and announcements.
    """
    model = RoomType
    template_name = "renthub/home.html"
    context_object_name = "room_types"

    def get_queryset(self):
        """Returns a queryset of distinct RoomType instances that have associated rooms."""
        return RoomType.objects.filter(room__isnull=False).distinct()

    def get_context_data(self, **kwargs):
        """Adds announcements to the context for rendering the home page."""
        context = super().get_context_data(**kwargs)
        context['announcement'] = Announcement.objects.all().order_by('-publish_date')
        return context
