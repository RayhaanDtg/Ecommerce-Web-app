from rest_framework import serializers
from Cart.models import Cart
from products.models import Product
from Order.models import Order


class ProductSerializer(serializers.Serializer):
    class Meta:
        model=Product
        fields= '__all__'


class CartSerializer(serializers.Serializer):
    class Meta:
        model=Cart
        fields= '__all__'


class OrderSerializer(serializers.Serializer):
    class Meta:
        model=Order
        fields= '__all__'