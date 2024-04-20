import json
import random
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
import requests
from bs4 import BeautifulSoup
from .models import *
from .forms import *
def index(request):
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        user_carts = Cart.objects.filter(session_id = request.session.session_key)
    products = Product.objects.all()
    products_count_in_cart = sum([cart.quantity for cart in user_carts])
    user_products = [cart.product.id for cart in user_carts]
    products_on_page = products.count()
    sizes = Size.objects.all()
    manufacturers = Manufacturer.objects.all()
    drawings = Drawing.objects.all()
    rooms = Room.objects.all()
    colors = Color.objects.all()
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products': products, 'title': 'Главная страница', 'user_products': user_products, 'products_in_cart': products_count_in_cart, 'products_on_page': products_on_page, 'sizes': sizes, 'manufacturers': manufacturers, 'drawings': drawings, 'rooms': rooms, 'colors': colors, 'page_obj': page_obj, }
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





def user_cart(request):
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user = request.user)
    else:
        user_carts = Cart.objects.filter(session_id = request.session.session_key)
    products_in_cart = sum([cart.quantity for cart in user_carts])
    all_cart_sum = sum([cart.total_sum() for cart in user_carts])
    context = {'carts': user_carts, 'products_in_cart': products_in_cart, 'all_cart_sum': all_cart_sum}
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



def add_product_in_cart(request):
    print(request.session.session_key)
    product = get_object_or_404(Product, id = request.POST.get('product_id'))
    if request.user.is_authenticated:
        user_products = [cart.product.id for cart in Cart.objects.filter(user = request.user)]
    else:
        user_products = [cart.product.id for cart in Cart.objects.filter(session_id = request.session.session_key)]
    if product.id not in user_products:
        if request.user.is_authenticated:
            Cart.objects.create(user = request.user, product = product, quantity = 1)
        else:
            Cart.objects.create(session_id = request.session.session_key, quantity = 1, product = product)
        info = 'Товар уже в корзине!'
    else:
        if request.user.is_authenticated:
            cart = Cart.objects.get(product = product, user = request.user)
            cart.delete()
        else:
            cart = Cart.objects.get(session_id = request.session.session_key, product = product)
            cart.delete()
        info = 'Добавить в корзину'
    if request.user.is_authenticated:
        products_in_cart = sum([cart.quantity for cart in Cart.objects.filter(user = request.user)])
    else:
        products_in_cart= sum([cart.quantity for cart in Cart.objects.filter(session_id = request.session.session_key)])
    return JsonResponse({'products_in_cart': products_in_cart, 'info': info})




def update_cart(request):
    product = Product.objects.get(id = request.POST.get('product_id'))
    if request.user.is_authenticated:
        cart = Cart.objects.get(product_id = product.id, user = request.user)
    else:
        cart = Cart.objects.get(product_id = product.id, session_id = request.session.session_key)
    cart.quantity = int(request.POST.get('quantity'))
    cart.save()
    cart_summ = cart.total_sum()
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user = request.user)
    else:
        user_carts = Cart.objects.filter(session_id = request.session.session_key)
    products_in_cart = sum([cart.quantity for cart in user_carts])
    products_in_cart_all = sum([cart.quantity for cart in user_carts])
    total_summ = sum([cart.total_sum() for cart in user_carts])
    return JsonResponse({'cart_summ': cart_summ, 'total_summ': total_summ, 'products_in_cart': products_in_cart, 'products_in_cart_all':products_in_cart_all })




def filter_products(request):
    room = request.GET.getlist('room')
    if not room:
        room = Room.objects.all()
    size = request.GET.getlist('size')
    if not size:
        size = Size.objects.all()
    manufacturer = request.GET.getlist('manufacturer')
    if not manufacturer:
        manufacturer = Manufacturer.objects.all()
    draw = request.GET.getlist('draw')
    if not draw:
        draw = Drawing.objects.all()
    color = request.GET.getlist('color')
    if not color:
        color = Color.objects.all()
    numberik1 = request.GET.get('numberik1', '0')
    numberik2 = request.GET.get('numberik2', '150')
    min_number = Decimal(numberik1)
    max_number = Decimal(numberik2)
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user=request.user)
    else:
        user_carts = Cart.objects.filter(session_id=request.session.session_key)
    products = list(set(Product.objects.filter(price__gte = min_number, price__lte = max_number, color__in = color, drawing__in = draw, room__in = room, size__in = size, manufacturer__in = manufacturer )))
    products_count_in_cart = sum([cart.quantity for cart in user_carts])
    user_products = [cart.product.id for cart in user_carts]
    products_on_page = len(products)
    manufacturers = Manufacturer.objects.all()
    drawings = Drawing.objects.all()
    rooms = Room.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    if products:
        paginator = Paginator(products, len(products))
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = []
    context = {'products': products, 'page_obj': page_obj, 'title': 'Главная страница', 'user_products': user_products, 'products_in_cart': products_count_in_cart, 'products_on_page': products_on_page, 'sizes': sizes, 'manufacturers': manufacturers, 'drawings': drawings, 'rooms': rooms, 'colors': colors}
    return render(request, 'wellpaper/index.html', context = context)








def about_us(request):
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user = request.user)
    else:
        user_carts = Cart.objects.filter(session_id = request.session.session_key)
    products_in_cart = sum([cart.quantity for cart in user_carts])
    context = {'title': 'О нас', 'products_in_cart': products_in_cart}
    return render(request, 'wellpaper/aboutus.html', context = context)



def generate(request):
    if request.user.is_superuser:
        manufacturers = Manufacturer.objects.all()
        sizes = Size.objects.all()
        drawings = Drawing.objects.all()
        rooms = Room.objects.all()
        colors = Color.objects.all()
        prices = [12.2, 56.6, 87.79, 32.32, 99.99, 34, 56, 12, 43.43, 65.65, 57, 87.23, 50,97, 34.23, 67.89]
        images = ['static/images/detskiye.jpg','static/images/sea.jpg', 'static/images/spalnya.jpg', 'static/images/tswetochki.jpg', 'static/images/zelenye.jpg', 'static/images/spalnya1.webp', 'static/images/spalnya3.jpg' ]
        articles = [984562, 315901, 868389, 345687, 985249, 291683, 234563, 998345, 285198, 198305, 178305, 305489, 434212, 984562, 895436, 764098, 304776, 882956 ]
        titles = ['Belaya Skazka', 'Detskie v Spalny', 'Cherny Klever', 'Salfetochny Jor', 'Yosemite Park', 'Mark Qwanti', 'Detskiy-lepet', 'Kloy-Merin', 'Bardzo-top', 'Yorik-Pop', 'Erisman']
        for i in range(1,10):
            manufacture = random.choice(manufacturers)
            size = random.choice(sizes)
            draw = random.choice(drawings)
            room = random.choice(rooms)
            color = random.choice(colors)
            image = random.choice(images)
            articl = random.choice(articles)
            price = random.choice(prices)
            title = random.choice(titles)
            product = Product.objects.create(manufacturer=manufacture, price=price, brand='Эскидр', title=title,
                                             image=image, size=size, drawing=draw, articl=articl,
                                             slug=title, quantity=100)
            product.room.set(random.sample(list(rooms), k=random.randint(1, 3)))
            product.color.set(random.sample(list(colors), k=random.randint(1, 3)))
            product.save()

        return redirect('index')
    else:
        return redirect('index')



def parsing(request):
    if request.user.is_superuser:
        page_number = 6
        for page in range(1, 3):
            if page == 0:
                response = requests.get('https://imperia-oboev.by/catalog/flizelinovye-oboi').text
            else:
                response = requests.get(f'https://imperia-oboev.by/catalog/flizelinovye-oboi?page={page_number}').text
            soap = BeautifulSoup(response, 'html.parser')
            all_items = soap.find_all('article', class_='card')
            for item in all_items:
                link = item.find('a').get('href')
                link_full = 'https://imperia-oboev.by' + str(link)
                response1 = requests.get(link_full).text
                soap1 = BeautifulSoup(response1, 'html.parser')
                price = float(soap1.find('span', class_='money js-price').text.replace('руб.', ' ').strip())
                info = soap1.find('div', class_='tab-content')
                params = info.find_all('td')
                params1 = soap1.find_all('span', class_='product_vendor')
                available = params1[0].text
                if available == 'В наличии':
                    available = True
                else:
                    available = False
                brand = params1[1].text
                title = str(soap1.find('h1', class_='title').text)
                articl = title.split(' ')[2]
                clear_brand = brand.replace('Бренд: ', '')
                size = params[0].text
                type = str(params[1].text)
                light = params[2].text
                if light == 'Нет':
                    light = False
                else:
                    light = True
                rooms = params[3].text
                rooms_clear = rooms.split(', ')
                draws = params[4].text
                draws_clear = draws.split(', ')
                colors = params[5].text
                colors_clear = colors.split(', ')
                image_div = soap1.find('div', id='featuted-image')
                image_link = image_div.find('a').get('href')
                image_content = requests.get(image_link).content
                image_name = f"{articl}_image.jpg"
                image_path = default_storage.save(f"media/wellpapers/{image_name}", ContentFile(image_content))
                product = Product.objects.create(
                    size = Size.objects.get(title = size),
                    price=price,
                    light=light,
                    available=available,
                    title=title,
                    image=image_path,
                    type = Type.objects.get(type = type),
                    manufacturer=Manufacturer.objects.get(title=clear_brand),
                    articl=articl,
                    slug=title
                )
                for room_name in rooms_clear:
                    room, _ = Room.objects.get_or_create(title=room_name)
                    product.room.add(room)
                for draw_name in draws_clear:
                    drawing, _ = Drawing.objects.get_or_create(title=draw_name)
                    product.drawing.add(drawing)
                for color_name in colors_clear:
                    color, _ = Color.objects.get_or_create(color=color_name)
                    product.color.add(color)
                product.save()
            page_number += 1
        return redirect('index')
    else:
        return redirect('index')



def product_detail(request, pk):
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user = request.user)
    else:
        user_carts = Cart.objects.filter(session_id = request.session.session_key)
    products_in_cart = sum([cart.quantity for cart in user_carts])
    product = Product.objects.get(id = pk)
    user_products = [cart.product.id for cart in user_carts]
    context = {'product': product, 'products_in_cart':products_in_cart, 'user_products': user_products }
    return render(request, 'wellpaper/product_detail.html', context = context)