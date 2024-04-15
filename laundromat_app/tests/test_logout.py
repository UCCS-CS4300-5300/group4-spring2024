from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class CustomLogoutViewTests(TestCase):
    def setUp(self):
        # Create a user
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
        
    def test_logged_in_user_can_successfully_logout(self):
        # Log in the user
        self.client.login(username='testuser', password='TestPassword123')
        
        # Make a POST request to the logout view
        response = self.client.post(reverse('logout'))
        
        # Check if the user is redirected to the home page after logging out
        self.assertRedirects(response, reverse('home_page'))


    def test_logged_out_user_redirected_to_home_page(self):
        # Make a GET request to the logout view
        response = self.client.post(reverse('logout'))
        
        # Check if the user is redirected to the home page after logging out
        self.assertRedirects(response, reverse('home_page'))

    def test_view_handles_logout_requests_correctly(self):
        # Log in the user
        self.client.login(username='testuser', password='TestPassword123')
        
        # Make a POST request to the logout view
        response = self.client.post(reverse('logout'))
        
        # Check if the user is redirected to the home page after logging out
        self.assertRedirects(response, reverse('home_page'))


    def test_user_remains_logged_out_after_logging_out(self):
        # Log in the user
        self.client.login(username='testuser', password='TestPassword123')
        
        # Make a POST request to the logout view
        self.client.post(reverse('logout'))
        
        # Attempt to access a protected page that requires authentication
        response = self.client.get(reverse('laundromat_create'))
        
        # Check if the user is redirected to the login page
        self.assertRedirects(response, reverse('unauthorized_view'))

