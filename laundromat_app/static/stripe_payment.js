// Retrieve the Stripe public key from the data attribute
var stripePublicKey = document.body.dataset.stripePublicKey;

// Create a Stripe client with the retrieved public key
var stripe = Stripe(stripePublicKey);

// Create an instance of Elements
var elements = stripe.elements();

// Create an instance of the card Element & mount onto div
var card = elements.create('card');
card.mount('#card-element');

var address = elements.create('address', {mode: 'billing',})
address.mount('#address-element');

// Handle real-time validation errors from the card Element
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle real-time validation errors from the card Element
address.addEventListener('change', function(event) {
  var displayError = document.getElementById('address-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  var email = document.getElementById('email').value;
  var billingDetails = {
    email: email,
    address: {
      city: document.getElementById('billing-city').value,
      country: document.getElementById('billing-country').value,
      line1: document.getElementById('billing-street').value,
      line2: '', // You can add the second line if needed
      postal_code: document.getElementById('billing-postal-code').value,
      state: document.getElementById('billing-state').value
    }
  };

  stripe.createToken(card,  billingDetails )
  .then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to stripe server
      stripeTokenHandler(result.token);
    }
  });
});

// Submit the form with the token ID
function stripeTokenHandler(token) {
  // Insert the token ID into the form so it gets submitted to the server
  var form = document.getElementById('payment-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);

  // Submit the form
  form.submit();
}