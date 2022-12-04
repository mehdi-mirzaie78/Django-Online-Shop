from django.db import models
from core.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name if self.user.full_name else self.user.phone_number


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=20)
    body = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.city} - {self.body}'
