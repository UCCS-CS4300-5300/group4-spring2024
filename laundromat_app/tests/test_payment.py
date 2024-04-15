from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class PaymentTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create a customer group
        self.customer_group = Group.objects.create(name='Customer')
        # Add the user to the customer group
        self.user.groups.add(self.customer_group)

    def test_payment_page_render(self):
        # Log in the user
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('process_payment'))
        # Check that the payment page renders successfully
        self.assertEqual(response.status_code, 200)
        # Check that the payment form is present
        self.assertContains(response, '<form method="POST" id="payment-form">')

    def test_successful_payment(self):
        # Log in the user
        self.client.login(username='testuser', password='password')
        # Access the payment page w/ test entries
        response = self.client.post(reverse('process_payment'), {
            'stripeToken': 'tok_visa',
            'cardholder-name': 'Test User',
            'email': 'test@example.com',
            'billing-street': '123 Test Street',
            'billing-city': 'Test City',
            'billing-state': 'California',
            'billing-country': 'United States'
        })
        # Check that the payment is successful and redirects to the success page
        self.assertRedirects(response, reverse('successful_payment'))

    def test_invalid_payment_info(self):
        # Log in the user
        self.client.login(username='testuser', password='password')

        # Attempt to make a payment with invalid information
        response = self.client.post(reverse('process_payment'), {
            'stripeToken': 'invalid_token',
            'cardholder-name': '',
            'email': 'invalid_email',
            'billing-street': '',
            'billing-city': '',
            'billing-state': '',
            'billing-country': '',
        })

        # Check that the payment form is re-rendered with errors
        self.assertEqual(response.status_code, 200)


    def test_unauthorized_access_to_payment_page(self):
        # Access the payment page without logging in
        response = self.client.get(reverse('process_payment'))
        # Check that unauthorized users are redirected to the login page
        self.assertRedirects(response, '/unauthorized/')