from django.urls import path, include
from rest_framework import routers

from rest_framework.routers import SimpleRouter
from products.views import ProductsViewList, ProductsViewDetail, OrderView


app_name = 'products'

router = SimpleRouter()

router.register(r"orders", OrderView, "Order")

urlpatterns = [
    path("products/", ProductsViewList.as_view()),
    path("products/<int:pk>", ProductsViewDetail.as_view()),
    path("", include(router.urls))

]