# Generated by Django 5.0.3 on 2024-03-11 16:29

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EcomApp', '0009_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='photos',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True),
        ),
    ]