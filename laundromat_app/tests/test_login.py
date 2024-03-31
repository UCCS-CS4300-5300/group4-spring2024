from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class CustomLoginViewTests(TestCase):
    def setUp(self):
        # Create the 'Owner' group if it doesn't exist
        if not Group.objects.filter(name='Owner').exists():
            Group.objects.create(name='Owner')

        self.login_url = reverse('login')  
        self.valid_credentials = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        }

        self.invalid_credentials = {
            'username': '',  # Invalid data, as username is required
            'email': 'invalid_email',  # Invalid email format
            'password1': 'password',  # Too short password
            'password2': 'password',
        }
        # Create a test user
        self.user = User.objects.create_user(
            username=self.valid_credentials['username'],
            email=self.valid_credentials['email'],
            password=self.valid_credentials['password1'],
        )

        # Assign the user to the 'Owner' group
        owner_group = Group.objects.get(name='Owner')
        self.user.groups.add(owner_group)

    #make sure we get the right form displaying for login
    def test_login_form_displayed_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_view_handles_login_requests_correctly(self):
        # Make a GET request to the login view
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

        # Make a POST request with valid credentials
        response = self.client.post(self.login_url, self.valid_credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

        # Make a POST request with invalid credentials
        response = self.client.post(self.login_url, self.invalid_credentials, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)