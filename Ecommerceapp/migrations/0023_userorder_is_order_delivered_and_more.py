# Generated by Django 4.1.4 on 2023-07-30 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0022_rename_product_userorder_product_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='is_order_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userorder',
            name='is_order_returned',
            field=models.BooleanField(default=False),
        ),
    ]
