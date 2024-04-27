// Retrieve the Stripe public key from the data attribute
var stripePublicKey = document.body.dataset.stripePublicKey;

// Create a Stripe client with the retrieved public key
var stripe = Stripe(stripePublicKey);

// Create an instance of Elements
var elements = stripe.elements();

// Create an instance of the card Element & mount onto div
var card = elements.create('card', {hidePostalCode: true});
card.mount('#card-element');

// Create an instance of the billing address Element & mount onto div
var address = elements.create('address', {mode: 'billing'});
address.mount('#address-element');

var billingAddress;
var city;
var country;
var line1;
var line2;
var postalCode;
var state;

// Handle real-time validation errors from the billing address Element
address.on('change', function(event) {
  billingAddress = event.value;
  fullName = billingAddress.name;
  city = billingAddress.city;
  country = billingAddress.country;
  line1 = billingAddress.line1;
  line2 = billingAddress.line2;
  postalCode = billingAddress.postal_code;
  state = billingAddress.state;
});


// Handle real-time validation errors from the card Element
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle real-time validation errors from the billing address Element
address.addEventListener('change', function(event) {
  var displayError = document.getElementById('address-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Retrieve the CSRF token from the cookie
function getCSRFToken() {
  var csrfToken = null;
  var cookies = document.cookie.split(';');
  for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.startsWith('csrftoken=')) {
          csrfToken = cookie.substring('csrftoken='.length, cookie.length);
          break;
      }
  }
  return csrfToken;
}

// Handle form submission
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  var email = document.getElementById('email').value;

  // Create a PaymentIntent
  fetch('/payment/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken()  // Include CSRF token in headers
    },
    body: JSON.stringify({
      email: email,
      city: city,
      country: country,
      line1: line1,
      postal_code: postalCode,
      state: state,
    }),
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    if (data.error) {
      // Handle errors
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = data.error;
    } else {
      // If no errors, confirm the PaymentIntent
      stripe.confirmCardPayment(data.client_secret, {
        payment_method: {
          card: card,
        }
      })
      .then(function(result) {
        if (result.error) {
          // Handle errors from Stripe.js
          var errorElement = document.getElementById('card-errors');
          errorElement.textContent = result.error.message;
        } else {
          // Redirect to the success page
          window.location.href = data.redirect_url;
        }
      });
    }
  });
});
