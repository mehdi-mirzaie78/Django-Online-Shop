from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from datetime import datetime, timedelta
import pytz
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from core.utils import phone_regex_validator


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_('Email'))
    phone_number = models.CharField(max_length=13, unique=True, validators=[phone_regex_validator],
                                    verbose_name=_('Phone Number'))
    full_name = models.CharField(max_length=50, verbose_name=_('Full Name'))
    is_active = models.BooleanField(default=True, verbose_name=_('Activation Status'))
    is_admin = models.BooleanField(default=False, verbose_name=_('Admin Status'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('Superuser Status'), help_text='')

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

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

    role.short_description = _('Role')


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=13, validators=[phone_regex_validator], verbose_name=_('Phone Number'))
    code = models.PositiveSmallIntegerField(verbose_name=_('Code'))
    created = models.DateTimeField(auto_now=True, verbose_name=_('Created'))

    class Meta:
        verbose_name = _('Otp Code')
        verbose_name_plural = _('Otp Codes')

    def save(self, *args, **kwargs):
        self.phone_number = '0' + self.phone_number[3:] if len(self.phone_number) == 13 else self.phone_number
        super(OtpCode, self).save(*args, **kwargs)

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
