# Generated by Django 5.0.1 on 2024-01-24 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EcomApp', '0004_cart_price_cart_unit_price_alter_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='unit_price',
        ),
    ]
