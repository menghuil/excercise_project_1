from django.contrib import admin

from product.models import Product, Shop


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock_pcs', 'price', 'shop', 'vip')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', )


admin.site.register(Product, ProductAdmin)
admin.site.register(Shop, ShopAdmin)
