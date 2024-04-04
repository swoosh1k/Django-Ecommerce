from django.contrib.auth.models import AbstractUser
from django.db import models

class Size(models.Model):
    title = models.CharField(max_length=140)


    def __str__(self):
        return f'размер {self.title}'

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

class Manufacturer(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return f'Производитель {self.title}'
    class Meta:
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'

class Drawing(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return f'Рисунок  {self.title}'
    class Meta:
        verbose_name = 'Drawing'
        verbose_name_plural = 'Drawings'




class Room(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return f'Помещение  {self.title}'
    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'



class Color(models.Model):
    color = models.CharField(max_length=150)

    def __str__(self):
        return f'Цвет  {self.color}'
    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

class Product(models.Model):
    price = models.DecimalField('Цена', max_digits = 6, decimal_places = 2, null = True)
    brand = models.CharField('Брэнд', max_length=150)
    title = models.CharField('название', max_length=150)
    image = models.ImageField(upload_to='wellpapers/')
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drawing = models.ForeignKey(Drawing, on_delete = models.CASCADE)
    room = models.ManyToManyField(Room)
    color = models.ManyToManyField(Color)
    articl  = models.CharField('артикуль', max_length=150)
    quantity = models.IntegerField('количество', default = 0)
    slug = models.SlugField('URL')


    def __str__(self):
        return f' Обои {self.title} с артикулем - {self.articl}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'



class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pic/', default = 'static/images/no_photo.jpg')


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_carts')
    product = models.ForeignKey(Product, on_delete = models.PROTECT, related_name = 'product_carts')
    quantity = models.SmallIntegerField()

    def __str__(self):
        return f'Cart {self.id} user: {self.user.username} product {self.product.title}'

    def total_sum(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class Order(models.Model):
    cart_data = models.JSONField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='orders')
    number = models.CharField('номер телефона', max_length=30)
    email = models.EmailField('email')
    message = models.CharField('сообщение', null = True, blank = True, max_length=30)

    def __str__(self):
        return f'id заказа: {self.id} номер телефона: {self.number}, {self.email}'

    class Meta:
        verbose_name_plural = 'заказы'
        verbose_name = 'заказ'



