# Generated by Django 4.1.4 on 2024-03-29 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0026_remove_usercart_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_name', models.CharField(default='', max_length=1000)),
                ('seller_email', models.EmailField(default='', max_length=1000)),
                ('seller_password', models.CharField(default='', max_length=1000)),
            ],
        ),
    ]
