from django.views.generic import ListView

from ..models import RoomType, Announcement


class HomeView(ListView):
    model = RoomType
    template_name = "renthub/home.html"
    context_object_name = "room_types"

    def get_queryset(self):
        return RoomType.objects.filter(room__isnull=False).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['announcement'] = Announcement.objects.all().order_by('-publish_date')
        return context
