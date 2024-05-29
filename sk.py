import stripe

def check_stripe_api(api_key):
    stripe.api_key = api_key
    try:
        # Retrieve account details
        account = stripe.Account.retrieve()
        account_country = account['country']
        capabilities = account.get('capabilities', {})

        # Check if the account allows checking card details directly
        card_payments_enabled = capabilities.get('card_payments', 'inactive')

        # Retrieve balance
        balance = stripe.Balance.retrieve()
        balance_amount = balance['available'][0]['amount']
        balance_currency = balance['available'][0]['currency']
        
        # Convert balance amount from cents to dollars (if applicable)
        balance_amount = balance_amount / 100

        print(f"API Key: {api_key}")
        print(f"Stripe API is working. Account country: {account_country}")
        print(f"Account balance: {balance_amount} {balance_currency.upper()}")
        print(f"Card payments capability: {card_payments_enabled}")
    except stripe.error.StripeError as e:
        print(f"API Key: {api_key}")
        print(f"Stripe API error: {e.user_message}")

def main():
    with open('api_keys.txt', 'r') as file:
        api_keys = file.readlines()
    
    for api_key in api_keys:
        api_key = api_key.strip()
        if api_key:  # Ensure the line is not empty
            check_stripe_api(api_key)

if __name__ == "__main__":
    main()
