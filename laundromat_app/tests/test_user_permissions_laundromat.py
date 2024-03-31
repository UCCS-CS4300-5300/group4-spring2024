from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from laundromat_app.models import Laundromat

class LaundromatPermissionTestCase(TestCase):
    def setUp(self):
        if not Group.objects.filter(name='Customer').exists():
            Group.objects.create(name='Customer')
    
        # Create a regular user (not in the 'Owner' group)
        self.user = User.objects.create_user(username='regular_user', password='password123')
        group = Group.objects.get(name='Customer')

        # Add the user to the group
        self.user.groups.add(group)

        # Create a laundromat owned by a different user
        self.laundromat = Laundromat.objects.create(name='Laundro1', location='Location1')
        self.owner_user = User.objects.create_user(username='owner_user', password='password456')
        self.laundromat.owner = self.owner_user
        self.laundromat.save()

    def test_unauthorized_user_cannot_update_laundromat(self):
        # Log in as the regular user
        self.client.login(username='regular_user', password='password123')

        # Attempt to access the laundromat update page for the laundromat created by another user
        response = self.client.get(reverse('laundromat_update', kwargs={'pk': self.laundromat.pk}))

        # Ensure that the user is redirected to the unauthorized view
        self.assertRedirects(response, reverse('unauthorized_view'))

    def test_unauthorized_user_cannot_create_laundromat(self):
        # Log in as the regular user
        self.client.login(username='regular_user', password='password123')
        
        # Attempt to access the laundromat creation page
        response = self.client.get(reverse('laundromat_create'))
        
        # Ensure that the user is redirected to the unauthorized view
        self.assertRedirects(response, reverse('unauthorized_view'))

    def test_unauthorized_user_cannot_delete_laundromat(self):
        # Log in as the regular user
        self.client.login(username='regular_user', password='password123')

        # Attempt to access the laundromat delete page for the laundromat created by another user
        response = self.client.post(reverse('laundromat_delete', kwargs={'pk': self.laundromat.pk}))

        # Ensure that the user is redirected to the unauthorized view
        self.assertRedirects(response, reverse('unauthorized_view'))