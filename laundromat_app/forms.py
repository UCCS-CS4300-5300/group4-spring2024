from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django import forms
from .models import Machines, Laundromat

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    group = forms.ChoiceField(choices=[(group.name, group.name) for group in Group.objects.all()])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#a form used for creating a laundromat in the app
class LaundromatForm(forms.ModelForm):
    class Meta:
        model = Laundromat
        fields = ['name', 'location', 'hours', 'description']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': '200'}),
                              label='Leave a message for our team')

# for creating/editing associated laundromat (NOT RESVERATION!)
class MachineForm(forms.ModelForm):
    class Meta:
        model = Machines
        fields = ['laundromat', 'machine_ID', 'machine_choice', 'status']
        #hide the laundromat field in the form
        widgets = {
            'laundromat': forms.HiddenInput(),
            'status': forms.HiddenInput()
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['machine', 'start_time']

