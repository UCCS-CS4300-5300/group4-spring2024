from django.test import TestCase
from .models import Machines, Laundromat
from django.urls import reverse
#used for api callings and testing 
from unittest.mock import patch, MagicMock
from .views import laundromat_listing


class URLTest(TestCase):
    def test_app_urls(self):
        # Access home page
        home_url = reverse('home_page')
        response = self.client.get(home_url)
        
        self.assertEqual(response.status_code, 200)

class LaundromatTest(TestCase):
    
    #creating a fake test laundromat doesn't go into DB
    def setUp(self):
        self.laundromat = Laundromat.objects.create(name="Test Laundromat", location = "Hawaii", \
            hours = "everyday", description = "cool place")

    def test_new_user(self):
        self.assertEqual(self.laundromat.name, "Test Laundromat")
        self.assertEqual(self.laundromat.location, "Hawaii")
        self.assertEqual(self.laundromat.hours, "everyday")
        self.assertEqual(self.laundromat.description, "cool place")

    #  creating a machine instance and saving it to the DB
    def test_create_machine(self):
        machine = Machines.objects.create(
            laundromat=self.laundromat,
            machine_ID="1",
            machine_choice=Machines.Dryer,
            status=Machines.Open
            )
        self.assertIsInstance(machine, Machines)

    #testing deafult machine availability
    def test_machine_default_availability (self):
        machine = Machines.objects.create(
            laundromat=self.laundromat,
            machine_ID="1",
            machine_choice=Machines.Dryer
        )
        self.assertEqual(machine.status, Machines.Open)

class LaundromatListingViewTests(TestCase):
    @patch('requests.get')
    def test_laundromat_listing_realistic_search(self, mock_get):
        # Mock responses for a realistic search ("Austin") and a search that has no location gibberish
        mock_responses = {
            'Austin': MagicMock(status_code=200, json=lambda: {
                'status': 'OK',
                'results': [{'geometry': {'location': {'lat': 30.267153, 'lng': -97.743061}}}]}),
            'JFGJDFGJFJG': MagicMock(status_code=200, json=lambda: {'status': 'ZERO_RESULTS'})
        }

        # Function to choose the response based on the input URL
        def get_response(url, *args, **kwargs):
            if 'Austin' in url:
                return mock_responses['Austin']
            else:
                return mock_responses['JFGJDFGJFJG']

        mock_get.side_effect = get_response

        # Test with a real location
        response_austin = self.client.get(reverse('laundromat_listing') + '?q=Austin')
        self.assertEqual(response_austin.status_code, 200)
        self.assertIn('Laundromats Near You', response_austin.content.decode())

        # Test with a gibberish string
        response_random = self.client.get(reverse('laundromat_listing') + '?q=JFGJDFGJFJG')
        self.assertEqual(response_random.status_code, 200)
        self.assertIn('No laundromats found for your search. Please try again.', response_random.content.decode())
