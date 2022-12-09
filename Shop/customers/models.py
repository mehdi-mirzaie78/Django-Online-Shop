from django.db import models
from accounts.models import User
from core.models import BaseModel


# Each user can be a customer too but not necessarily
class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='customers/', null=True, blank=True)

    def __str__(self):
        return self.user.full_name if self.user.full_name else self.user.phone_number


class Address(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=20)
    body = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.city} - {self.body}'
