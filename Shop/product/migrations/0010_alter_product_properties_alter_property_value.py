# Generated by Django 4.1.3 on 2022-12-11 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_rename_property_product_properties'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='properties',
            field=models.ManyToManyField(related_name='p_products', to='product.property'),
        ),
        migrations.AlterField(
            model_name='property',
            name='value',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]