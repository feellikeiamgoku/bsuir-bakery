from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login
from product_views.forms import LoginForm, RegisterForm

from products.models import Product

def index(request):
    return render(request, "product_views/index.html")


class ListProducts(generic.ListView):
    template_name = 'product_views/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()

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
