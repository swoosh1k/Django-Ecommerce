import json

from django.db.models.signals import post_delete, post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Order, Product
import telebot

@receiver(post_save, sender = Order)
def print_telebot(sender,  instance, created, **kwargs):
    if created:
            bot = telebot.TeleBot('7127890351:AAFEWmzyAr4CJODSuFvwGJ57ZTQHqutoYJg')
            number = instance.number
            email = instance.email
            user_message = instance.message
            cart_data = json.loads(instance.cart_data)
            order = ''
            total_summ = 0
            for key in cart_data:
                order += f"{cart_data[key]['product']} , количество: {cart_data[key]['quantity']} \n"
                total_summ += (int(cart_data[key]['quantity']) * int(Product.objects.filter(title = cart_data[key]['product']).first().price))
            message = f'Заказ обоев: номер телефона: {number} \nemail: {email} \nСообщение: {user_message} \nЗаказ: {order} \n Общая сумма заказа: {total_summ} '
            bot.send_message(545589900, message)
