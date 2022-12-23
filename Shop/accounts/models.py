from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from datetime import datetime, timedelta
import pytz
from django.core.validators import RegexValidator
from core.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    mobile_regex = RegexValidator(
        regex=r'^(\+989|09)+\d{9}$',
        message="Phone number can be one of these forms: +989XXXXXXXXX | 09XXXXXXXXX")
    phone_number = models.CharField(max_length=13, unique=True, validators=[mobile_regex])
    full_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True, verbose_name='Activation Status')
    is_admin = models.BooleanField(default=False, verbose_name='Admin Status')
    is_superuser = models.BooleanField(default=False, verbose_name='Superuser Status', help_text='')

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.phone_number = '0' + self.phone_number[3:] if len(self.phone_number) == 13 else self.phone_number
        super(User, self).save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.is_admin

    def role(self):
        return "Super User" if self.is_superuser else self.groups.get()

    role.short_description = 'Role'


class OtpCode(models.Model):
    mobile_regex = RegexValidator(
        regex=r'^(\+989|09)+\d{9}$',
        message="Phone number can be one of these forms: +989XXXXXXXXX | 09XXXXXXXXX")
    phone_number = models.CharField(max_length=13, validators=[mobile_regex])
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    @classmethod
    def is_code_available(cls, phone_number):
        counter = cls.objects.filter(phone_number=phone_number).count()
        return False if counter > 5 else True

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'

    def is_valid(self):
        utc = pytz.UTC
        expire = self.created + timedelta(minutes=32, hours=3)
        checked_on = datetime.now().replace(tzinfo=utc)
        expired_on = expire.replace(tzinfo=utc)
        if expired_on > checked_on:
            return True
        self.delete()
        return False
