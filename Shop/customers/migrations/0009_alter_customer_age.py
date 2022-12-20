# Generated by Django 4.1.3 on 2022-12-19 14:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_alter_customer_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(14), django.core.validators.MaxValueValidator(100)]),
        ),
    ]