from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse
from laundromat_app.forms import SignUpForm  
from laundromat_app.views import Signup  


class SignupViewTests(TestCase):
    def setUp(self):
        # Create the 'Owner' group if it doesn't exist
        if not Group.objects.filter(name='Owner').exists():
            Group.objects.create(name='Owner')

        self.signup_url = reverse('signup')
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
            'group': 'Owner'  # Assuming 'Owner' is one of the groups
        }
        self.assertTrue(Group.objects.filter(name='Owner').exists())
        self.invalid_data = {
            'username': '',  # Invalid data, as username is required
            'email': 'invalid_email',  # Invalid email format
            'password1': 'password',  # Too short password
            'password2': 'password',
            'group': 'Owner'  # Invalid group name
        }

    #make sure the signup form displays as intended
    def test_signup_form_displayed_correctly(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertIsInstance(response.context['form'], SignUpForm)

    #tests signup functionality with valid data
    def test_user_can_sign_up_with_valid_data(self):
        response = self.client.post(self.signup_url, self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('home_page'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    #makes sure the page redirects correctly after signing up
    def test_user_redirected_to_home_page_after_signing_up(self):
        response = self.client.post(self.signup_url, self.valid_data, follow=True)
        self.assertRedirects(response, reverse('home_page'))

    #make sure the group was set correctly
    def test_appropriate_group_assigned_to_user_after_signing_up(self):
        response = self.client.post(self.signup_url, self.valid_data, follow=True)
        self.assertTrue(Group.objects.get(name='Owner').user_set.filter(username='testuser').exists())

    #make sure invalid data gets error messages
    def test_form_validation_works_correctly_for_invalid_data(self):
        response = self.client.post(self.signup_url, self.invalid_data)
        self.assertEqual(response.status_code, 200)  # Ensure the form is re-rendered with errors

        # Check if the form is present in the response context
        form = response.context['form']
        self.assertTrue(form.errors)
