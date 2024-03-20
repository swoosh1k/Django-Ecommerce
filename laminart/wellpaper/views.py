import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView

from .models import *
from .forms import *

@login_required
def index(request):
    user = request.user
    products = Product.objects.all()
    products_in_cart = sum([cart.quantity for cart in Cart.objects.filter(user = request.user)])
    user_products = [cart.product.id for cart in Cart.objects.filter(user = request.user)]
    context = {'products': products, 'user': user, 'title': 'Главная страница', 'user_products': user_products, 'products_in_cart': products_in_cart}
    return render(request, 'wellpaper/index.html', context = context )



class UserLogin(LoginView) :
    template_name = 'wellpaper/login.html'
    form_class = UserLogin
    model = User

    def get_context_data(self,*, object_list = None,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'login'
        return context

class UserRegister(CreateView):
    model = User
    template_name = 'wellpaper/register.html'
    form_class = UserRegistretion

    def get_context_data(self,*, object_list = None,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'registretion'
        return context



def add_to_cart(request, pk):
    Cart.objects.create(product = get_object_or_404(Product, id = pk), user = request.user, quantity = 1)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



def user_cart(request):
    carts = Cart.objects.filter(user = request.user)
    products_in_cart = sum([cart.quantity for cart in carts])
    all_cart_sum = sum([cart.total_sum() for cart in carts])
    context = {'carts': carts, 'products_in_cart': products_in_cart, 'all_cart_sum': all_cart_sum}
    return render(request, 'wellpaper/cart.html', context = context)



def create_order(request):
    carts = Cart.objects.filter(user = request.user)
    cart_data = {}
    for cart in carts:
        cart_data[cart.id] = {
            'product': cart.product.title,
            'quantity': cart.quantity,
            'user': cart.user.username,
        }
    cart_data_json = json.dumps(cart_data)
    Order.objects.create(user = request.user, number = request.POST.get('number'), email  =request.POST.get('email'), message = request.POST.get('message'), cart_data = cart_data_json)
    carts.delete()
    messages.success(request, 'Спасибо, ваш заказ отправлен. Наш менеджер скоро свяжется с вами')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




def delete_item(request, pk):
    cart = Cart.objects.get(user = request.user, product_id = pk)
    cart.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
