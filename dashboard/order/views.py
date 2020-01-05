from rest_framework import mixins, viewsets

from order.models import Order
from order.serializers import OrderSerializer
from order.utils import check_qualification, check_qty


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @check_qty
    @check_qualification
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete_order()
