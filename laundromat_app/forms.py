from django import forms
from .models import *
from .models import Machines
#from .models import Reservation #if we move on uncomment

#a form used for creating a laundromat in the app
class LaundromatForm(forms.ModelForm):
    class Meta:
        model = Laundromat
        fields = ['name', 'location']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': '200'}), label='Leave a message for our team')



#a form used for creating a laundromat in the app
class LaundromatForm(forms.ModelForm):
    class Meta:
        model = Laundromat
        fields = ['name', 'location']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': '200'}), label='Leave a message for our team')

# for creating/editing associated laundromat (NOT RESVERATION!)
class MachineForm(forms.ModelForm):
    class Meta:
        model = Machines
        fields = ['laundromat', 'machine_ID', 'machine_choice', 'status']

#uncomment if we move on, ideally we do a view with 45 time limit leaving time to swap or clean machines
#class ReservationForm(forms.ModelForm):
 #   class Meta:
  #      model = Reservation
   #     fields = ['machine', 'start_time']