import json

from django.db.models.signals import post_delete, post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Order
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
            for key in cart_data:
                order += f"{cart_data[key]['product']} , количество: {cart_data[key]['quantity']} \n"
            message = f'Заказ обоев: номер телефона: {number} \nemail: {email} \n Сообщение: {user_message} \n Заказ: {order} '
            bot.send_message(545589900, message)
