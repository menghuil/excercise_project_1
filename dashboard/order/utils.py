from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from product.models import Product
from order.models import Customer


# TODO: abstract decorators
def check_qualification(_func=None):
    def check(func):
        @wraps(func)
        def wrapper(viewset, *args, **kwargs):
            request = viewset.request
            product_id = request.data.get('product')
            customer_id = request.data.get('customer')
            if not is_customer_qualified(product_id, customer_id):
                return Response('此商品僅提供給 VIP 會員',
                                status=status.HTTP_400_BAD_REQUEST)
            return func(viewset, *args, **kwargs)
        return wrapper
    if _func:
        return check(_func)
    else:
        return check


def check_qty(_func=None):
    def check(func):
        @wraps(func)
        def wrapper(viewset, *args, **kwargs):
            request = viewset.request
            product_id = request.data.get('product')
            qty = request.data.get('qty')
            if not is_qty_valid(product_id, qty):
                return Response('商品數量不足',
                                status=status.HTTP_400_BAD_REQUEST)
            return func(viewset, *args, **kwargs)
        return wrapper
    if _func:
        return check(_func)
    else:
        return check


def is_customer_qualified(product_id, customer_id):
    try:
        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(id=customer_id)
    except (Product.DoesNotExist, Customer.DoesNotExist):
        return False

    return not product.vip or customer.vip


def is_qty_valid(product_id, qty):
    return Product.objects.filter(id=product_id, stock_pcs__gte=qty).exists()
