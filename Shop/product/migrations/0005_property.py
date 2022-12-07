# Generated by Django 4.1.3 on 2022-12-07 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=120)),
                ('value', models.CharField(max_length=255)),
                ('product', models.ManyToManyField(related_name='properties', to='product.product')),
            ],
        ),
    ]
