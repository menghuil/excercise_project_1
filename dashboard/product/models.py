from django.db import models
from django.db.models import Count, F, Sum
from django.db.models.functions import Coalesce


class ShopManager(models.Manager):
    def get_sale_statistics(self):
        sale_amount = Coalesce(Sum(F('products__orders__qty') * F('products__price')), 0)
        sale_volume = Coalesce(Sum('products__orders__qty'), 0)
        order_count = Coalesce(Count('products__orders__id'), 0)

        return self.values('code') \
            .annotate(sale_amount=sale_amount, sale_volume=sale_volume, order_count=order_count) \
            .values('code', 'sale_amount', 'sale_volume', 'order_count') \



class Shop(models.Model):
    objects = ShopManager()

    code = models.CharField(max_length=20,
                            blank=False, null=False)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.code


class ProductManager(models.Manager):
    def order_by_sale_volume(self):
        return self.annotate(sale_volume=Coalesce(Sum('orders__qty'), 0)) \
                   .order_by('-sale_volume')


class Product(models.Model):
    objects = ProductManager()

    stock_pcs = models.IntegerField(blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    shop = models.ForeignKey(Shop, related_name='products',
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    vip = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return str(self.id)
