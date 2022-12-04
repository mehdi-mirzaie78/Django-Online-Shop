# Generated by Django 4.1.3 on 2022-12-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('code', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
