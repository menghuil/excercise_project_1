from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'stock_pcs', 'price', 'shop', 'vip')

