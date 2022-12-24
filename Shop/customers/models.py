from django.db import models
from accounts.models import User
from core.models import BaseModel
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


# Each user can be a customer too, but not necessarily
class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', verbose_name=_('User'))
    CHOICES = [('male', 'MALE'), ('female', 'FEMALE')]
    gender = models.CharField(max_length=20, choices=CHOICES, default='male', verbose_name=_('Gender'))
    image = models.ImageField(null=True, blank=True, verbose_name=_('Image'))
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(14), MaxValueValidator(100)],
                                      verbose_name=_('Age'))

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return self.user.full_name

    def save(self, *args, **kwargs):
        male = 'male.png'
        female = 'female.png'
        if not self.image:
            self.image = male if self.gender == 'male' else female
        elif self.image and self.image in [male, female]:
            self.image = male if self.gender == 'male' else female
        super(Customer, self).save(*args, **kwargs)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')

    image_tag.short_description = _('Image')

    def image_tag_2(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')

    image_tag_2.short_description = ''

    def user_full_name(self):
        return self.user.full_name

    user_full_name.short_description = _('Full Name')

    def phone_number(self):
        return self.user.phone_number

    phone_number.short_description = _('Phone Number')


class Address(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses',
                                 verbose_name=_('Customer'))
    city = models.CharField(max_length=20, verbose_name=_('City'))
    body = models.TextField(max_length=120, verbose_name=_('Body'))
    postal_code = models.CharField(max_length=10, unique=True, verbose_name=_('Postal Code'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f'{self.city} - {self.body}'
