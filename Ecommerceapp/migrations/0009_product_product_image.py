# Generated by Django 4.1.4 on 2023-04-16 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0008_remove_product_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default='', upload_to='images'),
        ),
    ]
