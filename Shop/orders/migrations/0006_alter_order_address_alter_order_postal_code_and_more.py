# Generated by Django 4.1.3 on 2022-12-11 11:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_address_created_alter_address_updated_and_more'),
        ('orders', '0005_order_address_alter_order_body_alter_order_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_orders', to='customers.address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='postal_code',
            field=models.CharField(editable=False, max_length=10, validators=[django.core.validators.RegexValidator('\\d{10}', message='Invalid Postal code')]),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
