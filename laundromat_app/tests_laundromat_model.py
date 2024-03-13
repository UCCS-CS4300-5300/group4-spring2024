from django.test import TestCase
from .models import Machines, Laundromat
from django.urls import reverse


class LaundromatTest(TestCase):    
    #creating a fake test laundromat doesn't go into DB
    def setUp(self):
        self.laundromat = Laundromat.objects.create(name="Test Laundromat")

        # Set up a new user to test inputs
        self.home_page = Laundromat.objects.create(name = 'Bob Smith', location = 'Hawaii', hours = 'Mon-Fri 24/7', \
            description = 'very cool laundry place')
        
    # Test app urls
    def test_app_urls(self):
        # Access home page
        home_url = reverse('home_page')
        response = self.client.get(home_url)
        
        self.assertEqual(response.status_code, 200)
            
    # Test user data inputs
    def test_new_user(self):
        self.assertEqual(self.home_page.name, 'Bob Smith')
        self.assertEqual(self.home_page.location, 'Hawaii')
        self.assertEqual(self.home_page.hours, 'Mon-Fri 24/7')
        self.assertEqual(self.home_page.description, 'very cool laundry place')    
    
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
