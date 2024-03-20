# Generated by Django 4.2.10 on 2024-03-18 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wellpaper', '0003_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='carts',
        ),
        migrations.AddField(
            model_name='order',
            name='cart_data',
            field=models.JSONField(default=''),
            preserve_default=False,
        ),
    ]
