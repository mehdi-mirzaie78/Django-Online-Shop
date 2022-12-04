from django.db import models
from core.models import User


class Customer(User):
    is_customer = models.BooleanField(default=True)


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=20)
    body = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.city} - {self.body}'
