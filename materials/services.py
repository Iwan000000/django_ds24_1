import stripe

from django_ds24_1.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price(payment):
    product = stripe.Product.create(
        name=payment.course.title
    )

    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(payment.course.price) * 100,
        product=product.id,
    )
    print(price.id)
    return price.id




def create_stripe_session(price_id):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{
            "price": price_id,
            "quantity": 1
        }],
        mode="payment",
    )
    print(session.url, session.id)
    return session.url, session.id


# def create_stripe_price(payment):
#     product = stripe.Product.create(
#         name=payment.course.title
#     )
#
#     price = stripe.Price.create(
#         currency="rub",
#         unit_amount=int(payment.course.price) * 100,
#         product=product.id,
#     )
#     return price.id
#
# def create_stripe_session(price_id):
#     session = stripe.checkout.Session.create(
#         success_url="https://127.0.0.1:8000/",
#         line_items=[{
#             "price": price_id,
#             "quantity": 1
#         }],
#         mode="payment",
#     )
#
#     return session.url, session.id

# session = stripe.checkout.Session.create(
#   payment_method_types=['card'],
#   line_items=[{
#     'price': price.id,
#     'quantity': 1,
#   }],
#   mode='payment',
#   success_url='https://example.com/success',
#   cancel_url='https://example.com/cancel',
# )

# session = stripe.checkout.Session.retrieve(session.id)
# payment_status = session.payment_status