import json
from django.db import models

from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, HttpResponse
from product_views.forms import LoginForm, RegisterForm

from products.models import Case, Product, OrderProduct, Order, PaymentMethods, OrderStatuses, ProductCategory

import pdb 

def index(request):
    return render(request, "product_views/index.html")


class ListProducts(generic.ListView):
    template_name = 'product_views/products.html'
    context_object_name = 'products'

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all()
        queryset = self.filter_price(queryset)
        queryset = self.filter_category(queryset)
        
        return queryset

    def filter_category(self, queryset):
        categories = self.request.GET.getlist("categories")
        if categories:

            return queryset.filter(category__name__in=categories).distinct()
        return queryset

    def filter_price(self, queryset):
        price_ord = self.request.GET.get("price-ord")
        if price_ord:
            if price_ord == "asc":
                return queryset.order_by("price")
            elif price_ord == "desc":
                return queryset.order_by("-price")
        return queryset

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context["categories"] = ProductCategory.objects.all()
        return context

class DetailProducts(generic.DetailView):
    template_name = 'product_views/product.html'
    context_object_name = 'product'
    model = Product


def user_login(request):
    if request.user.is_authenticated:
        return redirect("product_views:menu")
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("product_views:menu")
    else:
        form = LoginForm()
    return render(request, 'product_views/auth/login.html', {'form': form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect("product_views:menu")

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.add_message(request, messages.INFO, "Ваш аккаунт успешно создан!")
            return redirect("product_views:login")
    else:
        form = RegisterForm()
    return render(request, 'product_views/auth/register.html', {'form': form})


@login_required
def add_to_cart(request):
    case = Case.objects.get(user=request.user)

    if request.method == "POST":
        product_id = request.POST["product_id"]
        quantity = request.POST.get("quantity", 1) or 1
        
        product = Product.objects.get(id=product_id)
        try:
            product_in_case = case.products.get(product_id=product)
            product_in_case.quantity += int(quantity)
            product_in_case.save()
        except OrderProduct.DoesNotExist:
            order_product = OrderProduct(product_id=product, quantity=quantity)
            order_product.save()
            case.products.add(order_product)

        return redirect(request.headers["Referer"])
    elif request.method == "GET":
        return render(request, "product_views/cart.html", {"cart": case, "payment_methods": PaymentMethods})
    
    elif request.method == "DELETE":
        products = case.products.all().delete()
        return redirect(request.headers["Referer"])


@login_required
def delete_item_from_cart(request, pk):
    if request.method == "POST":
        case = request.user.case
        order_product = case.products.get(id=pk)
        order_product.delete()
        return redirect("product_views:cart")
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def update_item_from_cart(request, pk):
    new_quantity = json.loads(request.body.decode("utf-8")).get("quantity")
    if request.method == "POST":
        case = request.user.case
        order_product = case.products.get(id=pk)
        order_product.quantity = int(new_quantity) if new_quantity else order_product.quantity
        order_product.save()
        return HttpResponse("success", status=200)
    else:
        return HttpResponseNotAllowed()


@login_required
def create_list_order(request):
    if request.method == "POST":
        case = request.user.case
        payment_method = request.POST["payment_method"]
        order = Order(user_id=request.user, payment_method=payment_method)
        order.save()
        for product in case.products.all():
            order.products.add(product)
        case.products.clear()
        return redirect("product_views:menu")
    elif request.method == "GET":
        orders = Order.objects.all().filter(user_id=request.user).exclude(status=OrderStatuses.REFUSED).order_by("-created")
        return render(request, "product_views/orders.html", {"orders": orders, "statuses": OrderStatuses})
    else:
        return HttpResponseNotAllowed(["POST", "GET"])


@login_required
def update_orders(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        new_status = request.POST.get("status") or order.status
        order.status = new_status
        order.save()
        return redirect("product_views:create_list_order")


@login_required
def detail_orders(request, pk):
    order = Order.objects.get(id=pk)
    if order.user_id == request.user or request.user.is_worker:
        if order.status != OrderStatuses.REFUSED:
            return render(request, "product_views/order_detail.html", {"order": order, "statuses": OrderStatuses})    
    return HttpResponseNotAllowed(["GET"])
