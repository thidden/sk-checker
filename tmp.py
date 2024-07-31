import stripe
from flask import Flask, request, jsonify, render_template_string

# Set your Stripe API keys
stripe.api_key = "##"
stripe_publishable_key = "##"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Stripe Payment</title>
        <script src="https://js.stripe.com/v3/"></script>
    </head>
    <body>
        <h1>Secure Payment Form</h1>
        <form action="/charge" method="post" id="payment-form">
            <div class="form-row">
                <label for="card-element">
                    Credit or debit card
                </label>
                <div id="card-element">
                    <!-- A Stripe Element will be inserted here. -->
                </div>
                <!-- Used to display form errors. -->
                <div id="card-errors" role="alert"></div>
            </div>
            <button>Submit Payment</button>
        </form>

        <script>
            var stripe = Stripe('{{ stripe_publishable_key }}');
            var elements = stripe.elements();

            var style = {
                base: {
                    color: '#32325d',
                    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                    fontSmoothing: 'antialiased',
                    fontSize: '16px',
                    '::placeholder': {
                        color: '#aab7c4'
                    }
                },
                invalid: {
                    color: '#fa755a',
                    iconColor: '#fa755a'
                }
            };

            var card = elements.create('card', {style: style});
            card.mount('#card-element');

            card.on('change', function(event) {
                var displayError = document.getElementById('card-errors');
                if (event.error) {
                    displayError.textContent = event.error.message;
                } else {
                    displayError.textContent = '';
                }
            });

            var form = document.getElementById('payment-form');
            form.addEventListener('submit', function(event) {
                event.preventDefault();

                stripe.createPaymentMethod({
                    type: 'card',
                    card: card,
                }).then(function(result) {
                    if (result.error) {
                        var errorElement = document.getElementById('card-errors');
                        errorElement.textContent = result.error.message;
                    } else {
                        stripeTokenHandler(result.paymentMethod.id);
                    }
                });
            });

            function stripeTokenHandler(paymentMethodId) {
                var form = document.getElementById('payment-form');
                var hiddenInput = document.createElement('input');
                hiddenInput.setAttribute('type', 'hidden');
                hiddenInput.setAttribute('name', 'stripeToken');
                hiddenInput.setAttribute('value', paymentMethodId);
                form.appendChild(hiddenInput);

                form.submit();
            }
        </script>
    </body>
    </html>
    ''', stripe_publishable_key=stripe_publishable_key)

@app.route('/charge', methods=['POST'])
def charge():
    try:
        payment_method_id = request.form['stripeToken']
        
        # Create a Payment Intent with automatic payment methods
        intent = stripe.PaymentIntent.create(
            amount=100,  # Amount in cents, e.g., $1.00
            currency="usd",
            payment_method=payment_method_id,
            confirm=True,
            automatic_payment_methods={
                "enabled": True,
                "allow_redirects": "never"  # Prevent redirects
            }
        )
        return jsonify({'success': True, 'message': 'Payment successful.'}), 200
    except stripe.error.CardError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
