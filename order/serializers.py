from .models import Order, OrderItem
from products.serializers import ProductSerializer
from rest_framework import serializers

class OrderItemSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'products', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'total', 'items']

class CheckoutSessionRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class CheckoutSessionResponseSerializer(serializers.Serializer):
    checkout_url = serializers.URLField()