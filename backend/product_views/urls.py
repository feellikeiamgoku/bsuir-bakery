from django.urls import path

from product_views.views import index, ListProducts, DetailProducts, user_login, user_register
app_name = 'products'


urlpatterns = [

    path("", index, name="index"),
    path("menu/", ListProducts.as_view(), name="menu"),
    path("menu/<int:pk>", DetailProducts.as_view(), name="menu_detail"),
    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
    
]