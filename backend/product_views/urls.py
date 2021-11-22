from django.urls import path

from product_views.views import (index, ListProducts, DetailProducts, 
user_login, user_register, add_to_cart, delete_item_from_cart, update_item_from_cart, create_order)
app_name = 'products'


urlpatterns = [

    path("", index, name="index"),
    path("menu/", ListProducts.as_view(), name="menu"),
    path("menu/<int:pk>", DetailProducts.as_view(), name="menu_detail"),
    path("cart/", add_to_cart, name="cart"),
    path("cart/<int:pk>/delete", delete_item_from_cart, name="delete_item_from_cart"),
    path("cart/<int:pk>/update", update_item_from_cart, name="update_item_from_cart"),

    path("order/", create_order, name="create_order"),

    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
    
]