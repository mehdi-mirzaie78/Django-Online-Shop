from django.db import models
from accounts.models import User
from core.models import BaseModel
from django.utils.html import mark_safe


# Each user can be a customer too, but not necessarily
class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CHOICES = [('male', 'MALE'), ('female', 'FEMALE')]
    gender = models.CharField(max_length=20, choices=CHOICES, )
    image = models.ImageField(upload_to='customers/', null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.full_name if self.user.full_name else self.user.phone_number

    def save(self, *args, **kwargs):
        male = 'default/male.png'
        female = 'default/female.png'
        if not self.image:
            self.image = male if self.gender == 'male' else female
        elif self.image and self.image in [male, female]:
            self.image = male if self.gender == 'male' else female
        super(Customer, self).save(*args, **kwargs)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')

    image_tag.short_description = 'Image'

    def user_full_name(self):
        return self.user.full_name

    user_full_name.short_description = 'Full Name'

    def phone_number(self):
        return self.user.phone_number

    phone_number.short_description = 'Phone Number'


class Address(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=20)
    body = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.city} - {self.body}'
