from django.contrib import admin

# Register your models here.
from products.models import Product, Order, OrderProduct, Case, ProductCategory, Review, ProductReview


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Case)
admin.site.register(ProductCategory)
admin.site.register(Review)
admin.site.register(ProductReview)