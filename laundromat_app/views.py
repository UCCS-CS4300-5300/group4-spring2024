from django.shortcuts import render
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.http import HttpResponse
from .forms import ContactForm, LaundromatForm, MachineForm
from .models import Laundromat, Machines  # Make sure we already created Laundromat model in models.py
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.conf import settings  # New import

from django.shortcuts import render
from django.conf import settings
import requests

def laundromat_listing(request):
    # user's search query (city or zip code)
    search_query = request.GET.get('q', '')
    
    # list to hold the laundromat data
    laundromats = []

    if search_query:
        #  (make sure to set it in your environment or settings file... I did both)
        api_key = settings.GOOGLE_API_KEY

        # building the Geocoding API request URL
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={search_query}&key={api_key}"
        
        # requesting to the Geocoding API
        geocode_response = requests.get(geocode_url).json()

        if geocode_response.get('status') == 'OK':
            # taking the latitude and longitude from the Geocoding API response
            location = geocode_response['results'][0]['geometry']['location']
            latitude, longitude = location['lat'], location['lng']

            # creating the Places API request URL
            places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type=laundry&key={api_key}"
            
            # request to the Places API
            places_response = requests.get(places_url).json()

            if places_response.get('status') == 'OK':
                # takes the places API response data to the laundromats list
                laundromats = places_response['results']

    # Render the template with the list of laundromats from above
    return render(request, 'laundromat_list.html', {'laundromat_list': laundromats})

#loads the home page view layout and infomation will be covered in template desgin
def home_page(request):
    return render(request, 'homepage.html')

#checks for all 3 fields to be filled in, if it is it sends a thank you message, if not leaves the form stil up
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
class LaundromatCreate(CreateView):
   model = Laundromat
   form_class = LaundromatForm
   template_name = 'laundromat_form.html'
   
   def get_success_url(self):
    return reverse('laundromat_list')

   def form_valid(self, form):
    # Save the form data to the database
    form.save()
    return super().form_valid(form)

#allows a user to edit an existing laundromat
class LaundromatUpdate(UpdateView):
    model = Laundromat
    form_class = LaundromatForm
    template_name = 'laundromat_update.html'

    def get_object(self, queryset=None):
        # Retrieve the Laundromat instance using the pk from URL parameters
        pk = self.kwargs.get('pk')
        return get_object_or_404(Laundromat, pk=pk)

    def get_initial(self):
        # Fetch the existing Laundromat instance
        laundromat = self.get_object()
        # Populate the form fields with the instance's current values
        return {'laundromat_name': laundromat.name, 'location': laundromat.location}

    def form_valid(self, form):
        # Save the form data to the database
        form.save()
        return super().form_valid(form)

class LaundromatDeleteView(DeleteView):
    model = Laundromat
    # Redirect URL after deletion
    success_url = reverse_lazy('laundromat_list')  
    # Template for confirmation page
    template_name = 'laundromat_confirm_delete.html'  



class LaundromatListView(generic.ListView):
   model = Laundromat
   template_name = 'laundromat_list.html'

class LaundromatDetailView(generic.DetailView):
   model = Laundromat
   template_name = 'laundromat_detail.html'

#view for the machine creation page
class MachineCreate(CreateView):
  model = Machines
  form_class = MachineForm
  template_name = 'machine_form.html'
  
  def get_success_url(self):
    return reverse('machine_list', kwargs={'pk': self.object.laundromat.pk})

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
    
class MachineUpdate(UpdateView):
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

  def get_success_url(self):
    # Redirect to the machine list page after successful update
    return reverse('machine_list', kwargs={'pk': self.object.laundromat.pk})
  
  def form_valid(self, form):
    # Save the form data to the database
    form.save()
    return super().form_valid(form)
  
    #for debugging the form not being saved
  def form_invalid(self, form):
    print(form.errors)
    response = super().form_invalid(form)
    return response


class MachineDeleteView(DeleteView):
    model = Machines
    # Template for confirmation page
    template_name = 'machine_confirm_delete.html' 

    def get_object(self, queryset=None):
      # Retrieve the specific machine object to be updated
      laundromat_id = self.kwargs.get('laundromat_pk')
      machine_id = self.kwargs.get('pk')
      machine = get_object_or_404(Machines, laundromat_id=laundromat_id, pk=machine_id)
      return machine 
    
    def get_success_url(self):
      return reverse_lazy('machine_list', kwargs={'pk': self.kwargs['laundromat_pk']})

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


