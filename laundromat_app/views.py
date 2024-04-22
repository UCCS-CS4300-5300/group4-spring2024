from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf import settings
from django.http import Http404
from django.contrib import messages
import requests
import stripe
from .forms import ContactForm, LaundromatForm, MachineForm, SignUpForm
from .models import Laundromat, Machines


class Signup(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home_page')


    def form_valid(self, form):
        group_name = form.cleaned_data['group']
        user = form.save()
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = 'home_page'  # Redirect to the home page after logout


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home_page')
    authentication_form = AuthenticationForm  # Set the authentication form

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # If the 'next' parameter is present, redirect to that URL after login
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()


def laundromat_listing(request):
    # user's search query (city or zip code)
    search_query = request.GET.get('q', '')

    # list to hold the laundromat data
    laundromats = []

    if search_query:
        # Use your environment variable or setting for the API key
        api_key = settings.GOOGLE_API_KEY

        # Building the Geocoding API request URL
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={search_query}&key={api_key}"

        # Requesting to the Geocoding API
        geocode_response = requests.get(geocode_url).json()

        if geocode_response.get('status') == 'OK':
            # Taking the latitude and longitude from the Geocoding API response
            location = geocode_response['results'][0]['geometry']['location']
            latitude, longitude = location['lat'], location['lng']

            # Creating the Places API request URL
            places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type=laundry&key={api_key}"

            # Request to the Places API
            places_response = requests.get(places_url).json()

            if places_response.get('status') == 'OK':
                # Takes the places API response data and add
                #to the laundromats list, including place_id
                laundromats = [
                    {
                        'name': place.get('name'),
                        'vicinity': place.get('vicinity'),
                        'place_id': place.get('place_id'),  # This is the new line
                    }
                    for place in places_response.get('results', [])
                ]

    # Render the template with the list of laundromats from above
    return render(request, 'laundromat_list.html', {'laundromat_list': laundromats})


class UnauthorizedView(TemplateView):
    template_name = 'unauthorized.html'

#loads the home page view layout and infomation will be covered in template desgin
def home_page(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Owner').exists():
            # Query laundromats owned by the current user
            laundromats = Laundromat.objects.filter(owner=request.user)

            # Fetch all machines for each laundromat
            for laundromat in laundromats:
                laundromat.machines = laundromat.machines_set.all()

            # Pass the queryset to the template context
            context = {
                'laundromats': laundromats
            }
            return render(request, 'owner_homepage.html', context)
        else:
            return render(request, 'homepage.html')
    else:
        # Handle anonymous users
        return render(request, 'homepage.html')

def machine_list(request):
    return render(request, 'machines.html')

def reserve_machine(request):
    return render(request, 'reserve_machine.html')

#checks for all 3 fields to be filled in,
#if it is it sends a thank you message, if not leaves the form stil up
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            return HttpResponse('/thank-you/')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def about(request):
    #the about page using the'about.html'template
    return render(request, 'about.html')

#view for the laundromat creation page

class LaundromatCreate(UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Laundromat
    form_class = LaundromatForm
    template_name = 'laundromat_form.html'


    def test_func(self):
        return self.request.user.groups.filter(name='Owner').exists()

    def handle_no_permission(self):
        # Customize the redirect behavior for unauthorized users
        return HttpResponseRedirect(reverse('unauthorized_view'))

    def get_success_url(self):
        return reverse('home_page')

    def form_valid(self, form):
        # Save the form data to the database
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

#allows a user to edit an existing laundromat
class LaundromatUpdate(UserPassesTestMixin, UpdateView):
    model = Laundromat
    form_class = LaundromatForm
    template_name = 'laundromat_update.html'

    def test_func(self):
        # Get the laundromat object being updated
        laundromat = self.get_object()
        # Check if the logged-in user is in the "Owner" group & also owner of laundromat
        return self.request.user.groups.filter(name='Owner').exists() and self.request.user == laundromat.owner

    def handle_no_permission(self):
        # Customize the redirect behavior for unauthorized users
        return HttpResponseRedirect(reverse('unauthorized_view'))


    def get_object(self, queryset=None):
        # Retrieve the Laundromat instance using the pk from URL parameters
        pk = self.kwargs.get('pk')
        return get_object_or_404(Laundromat, pk=pk)

    def get_initial(self):
        # Fetch the existing Laundromat instance
        laundromat = self.get_object()
        # Populate the form fields with the instance's current values
        return {'name': laundromat.name, 'location': laundromat.location,
                'hours': laundromat.hours, 'description': laundromat.description}

    def form_valid(self, form):
        # Save the form data to the database
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home_page')

class LaundromatDeleteView(UserPassesTestMixin, DeleteView):
    model = Laundromat
    # Redirect URL after deletion
    success_url = reverse_lazy('laundromat_list')
    # Template for confirmation page
    template_name = 'laundromat_confirm_delete.html'

    def test_func(self):
        # Get the laundromat object being updated
        laundromat = self.get_object()
        # Check if the logged-in user is in the "Owner" group & also owner of laundromat
        return self.request.user.groups.filter(name='Owner').exists() and self.request.user == laundromat.owner

    def handle_no_permission(self):
        # Customize the redirect behavior for unauthorized users
        return HttpResponseRedirect(reverse('unauthorized_view'))

    def get_success_url(self):
        return reverse('home_page')




class LaundromatListView(generic.ListView):
    model = Laundromat
    template_name = 'laundromat_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class LaundromatDetailView(generic.View):
    template_name = 'laundromat_detail.html'

    def get(self, request, *args, **kwargs):
        # Extract the place_id from the URL kwargs
        place_id = kwargs.get('place_id')
        if not place_id:
            raise Http404("Laundromat not found")

        api_key = settings.GOOGLE_API_KEY
        # Make sure you have GOOGLE_API_KEY in your settings

        # Fetch the laundromat details using the place_id
        place_details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
        response = requests.get(place_details_url).json()

        if response['status'] != 'OK':
            raise Http404("Laundromat details not found")

        place_details = response.get('result', {})

        # Setup the context for the template
        context = {
            'name': place_details.get('name'),
            'location': place_details.get('formatted_address'),
            # Static data for demonstration
            'hours': "9:00 AM - 9:00 PM",
            'description': "This is a placeholder description for the laundromat. Offering the best laundry services in town with state-of-the-art machines and eco-friendly detergents."
        }

        # Render the template with the context
        return render(request, self.template_name, context)


#view for the machine creation page
class MachineCreate(UserPassesTestMixin, CreateView):
    model = Machines
    form_class = MachineForm
    template_name = 'machine_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the laundromat object based on the URL parameter
        laundromat_id = self.kwargs.get('pk')
        laundromat = get_object_or_404(Laundromat, pk=laundromat_id)
        # Pass the laundromat name to the template context
        context['laundromat'] = laundromat
        return context

    def form_valid(self, form):
        # Get the laundromat object based on the URL parameter
        laundromat_id = self.kwargs.get('pk')
        laundromat = get_object_or_404(Laundromat, pk=laundromat_id)

        # Set the laundromat field in the form instance
        form.instance.laundromat = laundromat
        form.instance.status = 'Open'

        # Call the parent class's form_valid method to save the form data
        return super().form_valid(form)

    #for debugging the form not being saved
    def form_invalid(self, form):
        print(form.errors)
        response = super().form_invalid(form)
        return response

    def test_func(self):
        # Retrieve the laundromat ID from URL parameters
        laundromat_id = self.kwargs.get('pk')
        # Retrieve the laundromat object based on the ID
        laundromat = get_object_or_404(Laundromat, pk=laundromat_id)
        # Check if the logged-in user is an owner and owns the laundromat
        return self.request.user.groups.filter(name='Owner').exists() and laundromat.owner == self.request.user

    def handle_no_permission(self):
        # Customize the redirect behavior for unauthorized users
        return HttpResponseRedirect(reverse('unauthorized_view'))

    def get_success_url(self):
        return reverse('home_page')


class MachineUpdate(UserPassesTestMixin, UpdateView):
    model = Machines
    form_class = MachineForm
    template_name = 'machine_update.html'

    def get_object(self, queryset=None):
        # Retrieve the specific machine object to be updated
        laundromat_id = self.kwargs.get('laundromat_pk')
        machine_id = self.kwargs.get('pk')
        machine = get_object_or_404(Machines, laundromat_id=laundromat_id, pk=machine_id)
        return machine

    def get_initial(self):
        # Provide initial data for the form
        initial = super().get_initial()
        machine = self.get_object()
        # Populate the form fields with the instance's current values
        initial['laundromat'] = machine.laundromat
        initial['machine_ID'] = machine.machine_ID
        initial['machine_choice'] = machine.machine_choice
        initial['status'] = machine.status
        return initial

    def form_valid(self, form):
        # Save the form data to the database
        form.save()
        return super().form_valid(form)

      #for debugging the form not being saved
    def form_invalid(self, form):
        print(form.errors)
        response = super().form_invalid(form)
        return response

    def test_func(self):
        # Retrieve the laundromat ID from URL parameters
        laundromat_id = self.kwargs.get('laundromat_pk')
        # Retrieve the laundromat object based on the ID
        laundromat = get_object_or_404(Laundromat, pk=laundromat_id)
        # Check if the logged-in user is an owner and owns the laundromat
        return self.request.user.groups.filter(name='Owner').exists() and laundromat.owner == self.request.user

    def handle_no_permission(self):
        # Customize the redirect behavior for unauthorized users
        return HttpResponseRedirect(reverse('unauthorized_view'))

    def get_success_url(self):
        return reverse('home_page')



class MachineDeleteView(UserPassesTestMixin, DeleteView):
    model = Machines
    # Template for confirmation page
    template_name = 'machine_confirm_delete.html'

    def get_object(self, queryset=None):
        # Retrieve the specific machine object to be updated
        laundromat_id = self.kwargs.get('laundromat_pk')
        machine_id = self.kwargs.get('pk')
        machine = get_object_or_404(Machines, laundromat_id=laundromat_id, pk=machine_id)
        return machine

    def test_func(self):
        # Retrieve the laundromat ID from URL parameters
        laundromat_id = self.kwargs.get('laundromat_pk')
        # Retrieve the laundromat object based on the ID
        laundromat = get_object_or_404(Laundromat, pk=laundromat_id)
        # Check if the logged-in user is an owner and owns the laundromat
        return self.request.user.groups.filter(name='Owner').exists() and laundromat.owner == self.request.user

    def handle_no_permission(self):
        # Customize the redirect behavior for unauthorized users
        return HttpResponseRedirect(reverse('unauthorized_view'))

    def get_success_url(self):
        return reverse('home_page')


class MachineListView(generic.ListView):
    model = Machines
    template_name = 'machine_list.html'

    def get_queryset(self):
        # Get the laundromat object based on the URL parameter
        laundromat_id = self.kwargs.get('pk')
        laundromat = get_object_or_404(Laundromat, pk=laundromat_id)

        # Filter machines based on the laundromat
        queryset = Machines.objects.filter(laundromat=laundromat)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the laundromat object based on the URL parameter
        laundromat_id = self.kwargs.get('pk')
        laundromat = get_object_or_404(Laundromat, pk=laundromat_id)
        # Pass the laundromat name to the template context
        context['laundromat'] = laundromat

        # Add the machine_list queryset to the context
        context['machine_list'] = self.get_queryset()
        return context

class MachineDetailView(generic.DetailView):
    model = Machines
    template_name = 'machine_detail.html'
    context_object_name = 'machine'

    def get_object(self, queryset=None):
        # Get the primary key of the machine from the URL
        machine_pk = self.kwargs.get('pk')
        # Get the primary key of the laundromat from the URL
        laundromat_pk = self.kwargs.get('laundromat_pk')
        # Query the Machines model to get the specific machine
        # Filter by both machine_pk and laundromat_pk to ensure correct machine retrieval
        machine = Machines.objects.filter(pk=machine_pk, laundromat_id=laundromat_pk).first()
        return machine

class ProcessPayment(UserPassesTestMixin, TemplateView):
    template_name = "payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        context['stripe_public_key'] = stripe_public_key
        return context

    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if request.method == 'POST':
            # Retrieve payment details from the form
            token = request.POST.get('stripeToken')
            #amount = request.POST.get('amount')  # Amount in cents
            amount = 1000  # $10.00 in cents FOR TESTING
            description = 'Payment for laundry services'  # Description of the payment

            try:
                # Charge the customer's card using Stripe's API
                charge = stripe.Charge.create(
                    amount=amount,
                    currency='usd',
                    description=description,
                    source=token,
                )
                # If payment is successful, redirect to the payment success page
                return redirect('successful_payment')

            except stripe.error.CardError as e:
                # Display error message if there's an issue with the card
                messages.error(request, f'Error: {e.error.message}')

            except stripe.error.StripeError:
                # Display generic error message for other Stripe-related errors
                messages.error(request, 'Payment processing failed. Please try again later.')

        # Render the payment page template with the context
        return self.render_to_response(self.get_context_data())

    def test_func(self):
        # Check if the current user is in the "Customer" group
        return self.request.user.groups.filter(name='Customer').exists()

    def handle_no_permission(self):
        # Customize the redirect behavior for unauthorized users
        return HttpResponseRedirect(reverse('unauthorized_view'))

#redirect to success page when payment goes through
class SuccessfulPayment(UserPassesTestMixin, TemplateView):
    template_name = "success_payment.html"

    def test_func(self):
        # Check if the current user is in the "Customer" group
        return self.request.user.groups.filter(name='Customer').exists()

    def handle_no_permission(self):
        # Customize the redirect behavior for unauthorized users
        return HttpResponseRedirect(reverse('unauthorized_view'))

#if customer cancels payment instead of submitting it
class CancelPayment(UserPassesTestMixin, TemplateView):
    template_name = "cancel_payment.html"

    def test_func(self):
        # Check if the current user is in the "Customer" group
        return self.request.user.groups.filter(name='Customer').exists()

    def handle_no_permission(self):
        # Customize the redirect behavior for unauthorized users
        return HttpResponseRedirect(reverse('unauthorized_view'))
