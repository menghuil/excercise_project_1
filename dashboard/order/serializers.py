from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField(source='product.price')
    shop = serializers.ReadOnlyField(source='product.shop.code')

    class Meta:
        model = Order
        fields = ('id', 'product', 'qty', 'price', 'shop', 'customer')

    def create(self, validated_data):
        return Order.objects.create_order(**validated_data)
