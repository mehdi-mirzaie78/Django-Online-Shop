from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from datetime import datetime, timedelta
import pytz


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'

    def is_valid(self):
        utc = pytz.UTC
        expire = self.created + timedelta(minutes=32, hours=3)
        checked_on = datetime.now().replace(tzinfo=utc)
        expired_on = expire.replace(tzinfo=utc)
        print(f'{checked_on=}', f'{expired_on=}')
        if expired_on > checked_on:
            return True
        return False
