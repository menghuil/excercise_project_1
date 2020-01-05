from django.conf.urls import include, url
from rest_framework import routers

from order import views

order_routers = routers.DefaultRouter()
order_routers.register(r'orders',
                       views.OrderViewSet,
                       base_name='orders')

urlpatterns = [
    url(r'', include(order_routers.urls)),
]
