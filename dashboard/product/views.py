from rest_framework import mixins, viewsets

from product.constants import BEST_SELLER_LIMIT
from product.models import Product
from product.serializers import ProductSerializer


class ProductViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    model = Product
    queryset = Product.objects \
        .order_by_sale_volume()[:BEST_SELLER_LIMIT]
    serializer_class = ProductSerializer

