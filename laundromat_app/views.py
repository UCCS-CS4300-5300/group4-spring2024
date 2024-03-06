from django.shortcuts import render
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.http import HttpResponse
from .forms import ContactForm, LaundromatForm
from .models import Laundromat  # Make sure we already created Laundromat model in models.py
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

def laundromat_listing(request):
    # Retrieve all laundromat objects from the database
    laundromats = Laundromat.objects.all()
    
    # Pass the laundromats to the template
    # The template will need to iterate over each laundromat and display its details
    return render(request, 'laundromat_listing.html', {'laundromats': laundromats})


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

