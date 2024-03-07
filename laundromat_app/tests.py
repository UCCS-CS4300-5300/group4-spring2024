from django.test import TestCase
from django.urls import reverse
from laundromat_app.models import Laundromat

# Test if app URLs are accessible
class TestAppUrls(TestCase):
    def test_app_urls(self):
        # Access home page
        home_url = reverse('home_page')
        response = self.client.get(home_url)
        
        self.assertEqual(response.status_code, 200)
    
# Test user data inputs on home page
class TestLaundromat(TestCase):
    # Set up data for new user
    def setUp(self):
        #self.home_page = Laundromat.objects.create(name = 'Bob Smith', location = 'Hawaii')

        self.home_page = Laundromat.objects.create(name = 'Bob Smith', location = 'Hawaii', hours = 24, \
            description = 'very cool laundry place')
            
    # Test user data inputs
    def test_new_user(self):
        self.assertEqual(self.home_page.name, 'Bob Smith')
        self.assertEqual(self.home_page.location, 'Hawaii')
        self.assertEqual(self.home_page.hours, 24)
        self.assertEqual(self.home_page.description, 'very cool laundry place')


