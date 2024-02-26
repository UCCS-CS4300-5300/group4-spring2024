from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from .models import Laundromat  # Make sure we already created Laundromat model in models.py

def laundromat_listing(request):
    # Retrieve all laundromat objects from the database
    laundromats = Laundromat.objects.all()
    
    # Pass the laundromats to the template
    # The template will need to iterate over each laundromat and display its details
    return render(request, 'laundromat_listing.html', {'laundromats': laundromats})


#loads the home page view layout and infomation will be covered in template desgin
def home_page(request):
    return render(request, 'home.html')

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



