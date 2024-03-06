from django import forms
from .models import *

#a form used for creating a laundromat in the app
class LaundromatForm(forms.ModelForm):
    class Meta:
        model = Laundromat
        fields = ['name', 'location']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': '200'}), label='Leave a message for our team')
