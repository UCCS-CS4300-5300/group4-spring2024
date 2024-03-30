from django.test import TestCase
from .models import Machines, Laundromat
from django.urls import reverse

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
