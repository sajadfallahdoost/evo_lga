from rest_framework import serializers
from basket.models import OrderItem
from account.models import Address


class OrderDispatchSerializer(serializers.Serializer):
    # Order information
    order_id = serializers.IntegerField(source="id")
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    # User contact details
    user_name = serializers.CharField(source="user.get_full_name")
    user_phone = serializers.CharField(source="user.phone_number")
    user_email = serializers.EmailField(source="user.email", required=False)

    # Address information
    street = serializers.CharField(source="address.address_line1")
    city = serializers.CharField(source="address.city")
    state = serializers.CharField(source="address.state")
    postal_code = serializers.CharField(source="address.postal_code")
    country = serializers.CharField(source="address.country")

    # Order items
    items = serializers.SerializerMethodField()

    def get_items(self, order):
        return [
            {
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
            }
            for item in order.order_items.all()
        ]
