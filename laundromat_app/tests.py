from django.test import TestCase
from .models import Machines, Laundromat

#creating a fake test laundromat doesn't go into DB
def setUp(self):
    self.laundromat = Laundromat.objects.create(name="Test Laundromat")


#  creating a machine instance and saving it to the DB
def create_machine(self):
    machine = Machines.objects.create(
        laundromat=self.laundromat,
        machine_ID="1",
        machine_choice=Machines.Dryer,
        status=Machines.Open
        )
    self.assertIsInstance(machine, Machines)

#testing deafult machine availability
def machine_default_availability (self):
    machine = Machines.objects.create(
        laundromat=self.laundromat,
        machine_ID="1",
        machine_choice=Machines.Dryer
    )
    self.assertEqual(machine.status, Machines.Open)
