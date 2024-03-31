from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from laundromat_app.views import CustomLoginView

class CustomLoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')  
        self.home_page_url = reverse('home_page')  
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='TestPassword123')

    #make sure the login form is there
    def test_login_form_displayed_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    #check that user can login
    def test_user_can_successfully_log_in_with_valid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'TestPassword123'})
        self.assertRedirects(response, self.home_page_url)

    #check page redirect after logging in
    def test_user_redirected_to_home_page_after_logging_in(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'TestPassword123'}, follow=True)
        self.assertRedirects(response, self.home_page_url)

    #make sure user is being authenticated correctly
    def test_view_handles_login_requests_correctly(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'TestPassword123'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    #test the redirect functionality after logging in
    def test_redirect_to_next_url_after_successful_login(self):
        next_url = '/laundromats/create/'  
        response = self.client.get(self.login_url + '?next=' + next_url)
        self.assertContains(response, next_url)

    #Make sure an invalid user can't login
    def test_form_validation_works_correctly_for_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
