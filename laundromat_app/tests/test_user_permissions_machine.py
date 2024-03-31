from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from laundromat_app.models import Laundromat, Machines
from laundromat_app.views import MachineCreate

class MachineUserTestCase(TestCase):
    def setUp(self):
        # Create a 'Customer' group if it doesn't exist
        if not Group.objects.filter(name='Customer').exists():
            Group.objects.create(name='Customer')
        
        # Create a regular user (in the 'Customer' group)
        self.user = User.objects.create_user(username='regular_user', password='password123')
        group = Group.objects.get(name='Customer')
        self.user.groups.add(group)
        
        # Create an owner user
        self.owner_user = User.objects.create_user(username='owner_user', password='password456')
        
        # Create a laundromat owned by the owner user
        self.laundromat = Laundromat.objects.create(name='Laundro1', location='Location1', owner=self.owner_user)

        # Create a machine associated with the laundromat
        self.machine = Machines.objects.create(laundromat=self.laundromat, machine_ID='1233', machine_choice = 'Washer', status='Open')

        # URL for machine create view with laundromat ID as a parameter
        self.machine_create_url = reverse('machine_create', kwargs={'pk': self.laundromat.pk})

    def test_unauthorized_user_cannot_access_machine_create(self):
        # Log in as a regular user (not in the 'Owner' group)
        self.client.login(username='regular_user', password='password123')
        # Make a GET request to the machine create view
        response = self.client.get(self.machine_create_url)
        # Check if the response status code is 302 (redirected to unauthorized view)
        self.assertEqual(response.status_code, 302)
        # Check if the user is redirected to the unauthorized view
        self.assertRedirects(response, reverse('unauthorized_view'))

    def test_authorized_owner_can_access_machine_create(self):
        # Log in as the owner user
        self.client.login(username='owner_user', password='password456')
        # Make a GET request to the machine create view
        response = self.client.get(self.machine_create_url)
        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

    def test_regular_user_cannot_access_machine_update(self):
        # Log in as the regular user
        self.client.login(username='regular_user', password='password123')
        # Construct the machine update URL with appropriate parameters
        laundromat_pk = self.laundromat.pk  
        machine_pk = self.machine.pk  
        machine_update_url = reverse('machine_update', kwargs={'laundromat_pk': laundromat_pk, 'pk': machine_pk})
        # Make a GET request to the machine update view
        response = self.client.get(machine_update_url)
        # Check if the response status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)
        # Check if the regular user is redirected to the unauthorized view
        self.assertRedirects(response, reverse('unauthorized_view'))



