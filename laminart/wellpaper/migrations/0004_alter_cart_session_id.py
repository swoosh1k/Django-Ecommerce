# Generated by Django 5.0.4 on 2024-04-19 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wellpaper', '0003_cart_session_id_alter_cart_user_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='session_id',
            field=models.CharField(max_length=150, null=True),
        ),
    ]