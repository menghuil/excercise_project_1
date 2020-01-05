from django.conf.urls import include, url
from rest_framework import routers

from product import views

product_routers = routers.DefaultRouter()
product_routers.register(r'products',
                         views.ProductViewSet,
                         base_name='products')

urlpatterns = [
    url(r'', include(product_routers.urls)),
]
