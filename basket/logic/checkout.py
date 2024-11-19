from django.db import transaction
from basket.models import Basket, Order, OrderItem


def create_order_from_basket(user, address, logistic_cost=0.0):
    try:
        basket = Basket.objects.filter(user=user).first()
        if not basket or not basket.items.exists():
            return None

        total_price = sum(item.product.final_price * item.quantity for item in basket.items.all())
        discount_applied = 0  # or any discount logic if applicable

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                address=address,
                total_price=total_price,
                discount_applied=discount_applied,
                logistic_cost=logistic_cost,
                status="pending",
            )

            OrderItem.objects.bulk_create([
                OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.final_price)
                for item in basket.items.all()
            ])

            basket.items.all().delete()  # Clear basket after creating the order
            return order
    except Exception as e:
        print(f"Error in creating order from basket: {e}")
        return None
