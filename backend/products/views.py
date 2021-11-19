from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from products.permissions import IsOwnerOrAdmin
from products.models import Product, Order, OrderStatuses
from products.serializers import ProductSerializer, OrderSerializer, OrderSerializerCreate, OrderSerializerUpdate
import pdb


class ProductsViewList(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductsViewDetail(APIView):
    
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class OrderView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def list(self, request):
        user = request.user
        if user.is_staff or user.is_worker:
            orders = Order.objects.all()
        else:
            orders = Order.objects.all().filter(user_id=user)
            orders = [order for order in orders if order.status != OrderStatuses.REFUSED]
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        self.check_object_permissions(request, order)
        if order.status == OrderStatuses.REFUSED and not request.user.is_worker:
            return Response({"error": "Not found"}, 404)

        serilizer = OrderSerializer(order)
        return Response(serilizer.data)

    def create(self, request):
        user = request.user
        request.data["user_id"] = user.id
        serialzer = OrderSerializerCreate(data=request.data)
        if serialzer.is_valid(raise_exception=True):
            serialzer.save()
            return Response(serialzer.data)

    def delete(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        self.check_object_permissions(request, order)

        if request.user.is_worker or request.user.is_staff:
            order.delete()
            return Response({"message": f"Order delted"}, 204)

        if order.status == OrderStatuses.REFUSED:
            return Response({"detail": "Not found"}, 404)

        serializer = OrderSerializer(order)
        order.status = OrderStatuses.REFUSED
        order.save()
        return Response(serializer.data, 204)
    
    def partial_update(self, request, pk):
        worker = request.user.is_worker
        order = get_object_or_404(Order, id=pk)

        if order.status == OrderStatuses.REFUSED:
            return Response({"detail": "Not found"}, 404)
        
        self.check_object_permissions(request, order)
        serializer = OrderSerializerUpdate(order, request.data, partial=True)

        
        if serializer.is_valid(True):
            status = serializer.validated_data.get("status")
            if status is not None and status in OrderStatuses:
                if not worker and status != OrderStatuses.WAITING and status != OrderStatuses.REFUSED:
                    return Response({"details": "User can't change status, only to Refused"}, 403)
                    
            serializer.save()
            return Response(serializer.data, 200)