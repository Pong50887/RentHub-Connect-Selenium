from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from django.contrib import messages
from django.views.generic import ListView, DetailView

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from mysite import settings
from .forms import RenterSignupForm
from .models import Room, Rental, Renter, RoomType


class HomeView(ListView):
    model = RoomType
    template_name = "renthub/home.html"
    context_object_name = "room_types"

    def get_queryset(self):
        return RoomType.objects.filter(room__isnull=False).distinct()


class RoomTypeView(ListView):
    model = Room
    template_name = "renthub/roomtype.html"
    context_object_name = "rooms"

    def get_queryset(self):
        pass
        # Get the room type from the URL
        room_type = self.kwargs['room_type']
        return Room.objects.filter(room_type__type_name=room_type)


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
            if Rental.objects.filter(room=room).exists():
                messages.info(request, "This room is taken.")
            else:
                messages.error(request, "This room is currently unavailable.")
            return HttpResponseRedirect(reverse("renthub:home"))

        return super().get(request, *args, **kwargs)


class RoomPaymentListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "renthub/payment_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        rentals = Rental.objects.filter(renter__id=self.request.user.id)
        return Room.objects.filter(rental__in=rentals)


class RoomPaymentView(LoginRequiredMixin, DetailView):
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

        try:
            renter = Renter.objects.get(id=request.user.id)
        except Renter.DoesNotExist:
            renter = None
            messages.warning(request, "You need to register as a renter to proceed with a rental.")

        if Rental.objects.filter(room=room).exclude(renter=renter).exists():
            messages.error(request, "This room is already taken.")
            return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room.room_number}))

        rental_exists = Rental.objects.filter(room=room, renter=renter).exists()
        if rental_exists:
            messages.info(request, "You already have a rental for this room.")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            renter = Renter.objects.get(id=self.request.user.id)
        except Renter.DoesNotExist:
            renter = None

        context['rental_exists'] = Rental.objects.filter(room=context['room'], renter=renter).exists()

        return context


@login_required
def submit_payment(request, room_number):
    user = request.user
    if not user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    try:
        renter = Renter.objects.get(id=user.id)
    except Renter.DoesNotExist:
        messages.error(request, "You must be a registered renter to rent a room.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room_number}))

    try:
        room = Room.objects.get(room_number=room_number)
    except Room.DoesNotExist:
        messages.error(request, f"Room {room_number} does not exist.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room_number}))

    if Rental.objects.filter(room=room).exclude(renter=renter).exists():
        messages.error(request, "This room is already taken.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room.room_number}))

    rental_exists = Rental.objects.filter(room=room, renter=renter).exists()
    if rental_exists:
        messages.info(request, "You already rented this room")
        return render(request, "renthub/payment.html", {"room": room, "rental_exists": rental_exists})
    # month_difference = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
    # temporary version: if can submit and show in user's payment feature
    rental_fee = room.price * 1
    rental = Rental(room=room, renter=renter, rental_fee=rental_fee)
    rental.save()
    room.availability = False
    messages.info(request, "Your renting was successful")
    # check rental_exists again because it didn't exist before, but is now created
    rental_exists = Rental.objects.filter(room=room, renter=renter).exists()
    return render(request, "renthub/payment.html", {"room": room, "rental_exists": rental_exists})


@login_required
def cancel_rental(request, room_number):
    room = Room.objects.get(room_number=room_number)
    user = request.user
    if not user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    try:
        renter = Renter.objects.get(id=user.id)
    except Renter.DoesNotExist:
        messages.error(request, "You must be a registered renter to cancel a rental.")
        return HttpResponseRedirect(reverse("renthub:rental", kwargs={'room_number': room_number}))

    try:
        rental = Rental.objects.get(room=room, renter=renter)
        rental.delete()
        room.availability = True
        messages.info(request, "Your booking cancellation was successful.")
    except Rental.DoesNotExist:
        messages.warning(request, "You do not have an active booking for this room.")
    return render(request, "renthub/payment.html",
                  {"room": room, "rental_exists": Rental.objects.filter(room=room, renter=renter).exists()})


# Change this to View class
def renter_signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = RenterSignupForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password1')
            phone_number = form.cleaned_data.get('phone_number')  # Get phone number from form
            user = authenticate(username=username, password=raw_passwd)

            renter = Renter(phone_number=phone_number)
            renter.save()

            login(request, user)
            return redirect('renthub:home')
        else:
            messages.error(request, "This form is invalid")
    else:
        form = RenterSignupForm()
    return render(request, 'registration/signup.html', {'form': form})
