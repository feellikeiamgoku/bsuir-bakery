from django.urls import path

from product_views.views import (index, about, ListProducts, DetailProducts, 
user_login, user_register, add_to_cart, delete_item_from_cart, update_item_from_cart, create_list_order,
update_orders, detail_orders, contacts)
app_name = 'products'


urlpatterns = [

    path("", index, name="index"),
    path("about/", about, name="about"),
    path("contacts/", contacts, name="contacts"),
    path("menu/", ListProducts.as_view(), name="menu"),
    path("menu/<int:pk>", DetailProducts.as_view(), name="menu_detail"),
    path("cart/", add_to_cart, name="cart"),
    path("cart/<int:pk>/delete", delete_item_from_cart, name="delete_item_from_cart"),
    path("cart/<int:pk>/update", update_item_from_cart, name="update_item_from_cart"),

    path("order/", create_list_order, name="create_list_order"),
    path("order/<int:pk>/update", update_orders, name="update_orders"),
    path("order/<int:pk>/detail", detail_orders, name="detail_orders"),


    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
    
]