from django.urls import path, include
from .views import (OrderServicesView, CalculatorShipoxView, LocationsUZbUZbView, LocationsKrelUZbView, LocationsAllView, VIloyatuzbView, VIloyatkrlView, ResultExelView,
    CalculatorShipoxIndexView, LocationsKrelAllView, PostIndexesView, PostIndexesAllView)
from .create import CreateOrderApiView, CancelOrderAPIView, CreateOderIndexAPIView




urlpatterns = [
    path("order-price/", CalculatorShipoxView.as_view(), name='price-calculator'),
    path("order-price-index/", CalculatorShipoxIndexView.as_view(), name='price-index'),
    path("regions/uzb/", VIloyatuzbView.as_view(), name='viloyatlar'),
    path("regions/krl/", VIloyatkrlView.as_view(), name='viloyatlar_krl'),
    path("services/", OrderServicesView.as_view(), name='order-services'),
    path("locations-district/krel/", LocationsKrelUZbView.as_view(), name='locations-krel'),
    path("locations-district/uzb/", LocationsUZbUZbView.as_view(), name='locations-uzb'),
    path("locations-others/uzb/", LocationsAllView.as_view(), name='locations-all-uz'),
    path("locations-others/krel/", LocationsKrelAllView.as_view(), name='locations-all-krel'),
    path("results/", ResultExelView.as_view(), name='exel'),
    path("post/indexes/", PostIndexesView.as_view(), name='post-index'),
    path("post/indexes/all/", PostIndexesAllView.as_view(), name='post-indexes-all'),
    path("create/order/", CreateOrderApiView.as_view(), name='create-order'),
    path("create/order/index/", CreateOderIndexAPIView.as_view(), name='create-order-index'),
    path("cancel/order/", CancelOrderAPIView.as_view(), name='cancel-order')

]
