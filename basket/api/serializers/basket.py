from rest_framework import serializers
from basket.models import Basket, BasketItem, Order, OrderItem
from product.api.serializers import ProductSerializer


class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'quantity', 'added_at']


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Basket
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']
        read_only_fields = ['user']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'total_price', 'discount_applied', 'logistic_cost', 'status', 'created_at', 'updated_at', 'order_items']
        read_only_fields = ['user']
