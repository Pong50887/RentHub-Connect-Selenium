from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.contrib import messages

from ..models import PropertyOwner, Rental
from ..admin import MaintenanceRequestForm


class ContactUsView(DetailView):
    """
    View for displaying and submitting maintenance requests to admin.
    """
    model = PropertyOwner
    template_name = 'renthub/contact_us.html'
    context_object_name = 'contact'

    def get_object(self, **kwargs):
        """Retrieves the first instance of the PropertyOwner model."""
        return PropertyOwner.objects.first()

    def get_context_data(self, **kwargs):
        """Adds the maintenance request form to the context data."""
        context = super().get_context_data(**kwargs)
        context['maintenance_form'] = MaintenanceRequestForm()
        return context

    def post(self, request, *args, **kwargs):
        """Handles POST requests for submitting a maintenance request."""
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            rental = Rental.objects.filter(renter=request.user.id).first()
            if rental:
                form.save(rental=rental)
                messages.success(request, 'Maintenance request sent successfully.')
            else:
                messages.error(request, 'You do not have a rental associated with your account.')

            return redirect('renthub:contact_us')

        context = self.get_context_data()
        context['maintenance_form'] = form
        return self.render_to_response(context)
