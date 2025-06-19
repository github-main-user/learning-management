import stripe
from django.conf import settings
from stripe.checkout import Session

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name: str, description: str) -> str:
    """Creates a stripe product."""
    product = stripe.Product.create(name=name, description=description)
    return product.id


def create_stripe_price(product_id: str, amount: int) -> str:
    """Creates a price for a given product. Amount should be in penny."""
    price = stripe.Price.create(product=product_id, unit_amount=amount, currency="usd")
    return price.id


def create_stripe_checkout_session(
    price_id: str, success_url: str, cancel_url: str
) -> Session:
    """Creates a stripe checkout session."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


def fetch_stripe_session(session_id: str) -> Session:
    """Fetches and returns stripe session by a given id."""
    return stripe.checkout.Session.retrieve(session_id)
