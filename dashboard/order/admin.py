from django.contrib import admin

from order.models import Customer, Order


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'qty')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
