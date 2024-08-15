import stripe

class StripeManager:
    def __init__(self):
        self.stripe = stripe
        self.stripe.api_key = 'your_stripe_secret_key_here'

    def create_checkout_session(self, amount):
        try:
            checkout_session = self.stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(amount * 100),  # amount in cents
                        'product_data': {
                            'name': 'AI Image Model Training',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://ai-image-model-maker.com/success',
                cancel_url='https://ai-image-model-maker.com/cancel',
            )
            return checkout_session.id
        except Exception as e:
            print(f"Error creating checkout session: {str(e)}")
            return None