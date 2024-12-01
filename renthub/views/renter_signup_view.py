from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate

from ..forms import RenterSignupForm


class RenterSignupView(View):
    """
    Register a new user.
    """

    def get(self, request):
        """Display the signup form."""
        form = RenterSignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        """Process the submitted signup form."""
        form = RenterSignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            renter = form.save(commit=False)

            phone_number = form.cleaned_data.get('phone_number')
            renter.phone_number = phone_number
            renter.save()

            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)

            login(request, user)
            return redirect('renthub:home')
        else:
            messages.error(request, "This form is invalid")
            return render(request, 'registration/signup.html', {'form': form})
