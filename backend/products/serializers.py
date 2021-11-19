from django.core.exceptions import ValidationError
from django.http.response import HttpResponseBadRequest
from rest_framework.response import Response
from products.models import OrderStatuses, Product, Order, OrderProduct
from rest_framework.serializers import ModelSerializer, IntegerField

import pdb

# get serializers

class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
    

class OrderProductSerializer(ModelSerializer):
    product_id = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = "__all__"



class OrderSerializer(ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"


# create serializers

class OrderProductSerializerCreate(ModelSerializer):
    
    class Meta:
        model = OrderProduct
        fields = ["product_id", "quantity"]


class OrderSerializerCreate(ModelSerializer):
    products = OrderProductSerializerCreate(many=True)

    class Meta:
        model = Order
        fields = "__all__"
    

    def validate_products(self, data):
        if len(data) <= 0:
            raise ValidationError("You must set at least one proudct")
        return data
    
    def create(self, data):
        products_order_data = data.pop("products")
        order = Order.objects.create(**data)

        for order_product in products_order_data:
            products_order = OrderProduct.objects.create(**order_product)
            order.products.add(products_order)
        return order


class OrderProductSerializerUpdate(ModelSerializer):
    id = IntegerField()

    class Meta:
        model = OrderProduct
        fields = ["id", "product_id", "quantity"]

class OrderSerializerUpdate(ModelSerializer):
    products = OrderProductSerializerUpdate(many=True)

    class Meta:
        model = Order
        fields = "__all__"
    
    def update(self, instance, validated_data):
        pdb.set_trace()
        if instance.status not in [OrderStatuses.REFUSED, OrderStatuses.WAITING]:
            pdb.set_trace()
            instance.status = validated_data.get("status", instance.status)
            return instance
        else:
            instance.status = validated_data.get("status", instance.status)
            instance.payment_method = validated_data.get("payment_method", instance.payment_method)

            
            products = validated_data.get("products", [])
            try:
                for product in products:
                    inst_product = instance.products.get(id=product.get("id"))
                    inst_product.quantity = product.get("quantity")
                    inst_product.save()
                    
            except OrderProduct.DoesNotExist:
                raise HttpResponseBadRequest
            instance.save()
            return instance
