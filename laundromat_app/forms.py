from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': '200'}), label='Leave a message for our team')
