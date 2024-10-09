from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Room, Rental, Renter
from django.contrib import messages
from django.views.generic import ListView, DetailView

from mysite import settings

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = Room
    template_name = "renthub/home.html"
    context_object_name = "room_types"

    def get_queryset(self):
        return Room.objects.values_list('type', flat=True).distinct()


class RoomTypeView(ListView):
    model = Room
    template_name = "renthub/roomtype.html"
    context_object_name = "rooms"

    def get_queryset(self):
        # Get the room type from the URL
        room_type = self.kwargs['room_type']
        return Room.objects.filter(type=room_type)


class RoomListView(ListView):
    model = Room
    template_name = "renthub/rental_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.filter(availability=True)


class RoomDetailView(DetailView):
    model = Room
    template_name = "renthub/rental.html"
    context_object_name = "room"

    def get_object(self, queryset=None):
        room_number = self.kwargs.get("room_number")
        room = get_object_or_404(Room, room_number=room_number)
        return room

    def get(self, request, *args, **kwargs):
        try:
            room = self.get_object()
        except Http404:
            return HttpResponseRedirect(reverse("renthub:home"))

        if not room.availability:
            return HttpResponseRedirect(reverse("renthub:home"))

        return super().get(request, *args, **kwargs)


class RoomPaymentListView(LoginRequiredMixin,ListView):
    model = Room
    template_name = "renthub/payment_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.filter(availability=True)


class RoomPaymentView(LoginRequiredMixin,DetailView):
    model = Room
    template_name = "renthub/payment.html"
    context_object_name = "room"

    def get_object(self, queryset=None):
        room_number = self.kwargs.get("room_number")
        room = get_object_or_404(Room, room_number=room_number)
        return room

    def get(self, request, *args, **kwargs):
        try:
            room = self.get_object()
        except Http404:
            return HttpResponseRedirect(reverse("renthub:home"))

        if not room.availability:
            messages.error(request, f"The room {room} is currently unavailable.")
            return HttpResponseRedirect(reverse("renthub:home"))

        return super().get(request, *args, **kwargs)


@login_required
def submit_payment(request, room_number):
    room = Room.objects.get(room_number=room_number)
    user = request.user
    if not user.is_authenticated:
        # return redirect('login')
        # or, so the user comes back here after login...
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    # try:
    #     renter = Renter.objects.get(id=user.id)
    #     renter_id = renter.id
    # except Renter.DoesNotExist:
    #     messages.error(request, "You must be a registered renter to rent a room.")
    #     return HttpResponseRedirect(reverse("renthub:payment"))
    #
    # if Rental.objects.filter(room=room_id, renter=renter_id).exists():
    #     messages.info(request, "You have already rented this room.")

    return render(request, "renthub/payment.html", {"room": room})

def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('renthub:home')
        else:
            messages.error(request, "This form is invalid")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
