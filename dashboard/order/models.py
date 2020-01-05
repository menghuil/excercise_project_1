from django.db import models, transaction
from django.db.models import F

from common.tasks import send_mail
from product.models import Product, Shop


# TODO: move Customer to another app
class Customer(models.Model):
    name = models.CharField(max_length=50,
                            blank=False, null=False)
    vip = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.name


class OrderManager(models.Manager):

    def create_order(self, *args, **kwargs):
        with transaction.atomic():
            qty = kwargs.get('qty')
            product = kwargs.get('product')

            order = self.create(*args, **kwargs)
            Product.objects.filter(id=product.id) \
                .update(stock_pcs=F('stock_pcs') - qty)
        return order


class Order(models.Model):
    objects = OrderManager()

    customer = models.ForeignKey(Customer, related_name='orders',
                                 on_delete=models.CASCADE,
                                 blank=False, null=False)
    product = models.ForeignKey(Product, related_name='orders',
                                on_delete=models.SET_NULL,
                                blank=False, null=True)  # might be m2m field
    qty = models.IntegerField(blank=False, null=False)

    # created_at

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return str(self.id)

    def delete_order(self):
        to_notify = Product.objects.filter(id=self.product_id, stock_pcs=0).exists()
        with transaction.atomic():
            Product.objects.filter(id=self.product_id) \
                .update(stock_pcs=F('stock_pcs') + self.qty)
            self.delete()
        if to_notify:
            msg = f'商品 {self.product_id} 已有庫存'
            send_mail.s(subject=msg, message=msg).apply_async()
