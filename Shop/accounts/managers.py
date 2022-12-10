from django.contrib.auth.models import BaseUserManager
from django.core.validators import ValidationError
import re


class UserManager(BaseUserManager):

    def create_user(self, phone_number, email, full_name, password):
        if not phone_number:
            raise ValueError('user must have a phone number')

        if not email:
            raise ValueError('user must have an email')

        if not full_name:
            raise ValueError('user must have a full name')

        user = self.model(phone_number=self.normalize_phone_number(phone_number),
                          email=self.normalize_email(email),
                          full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, full_name, password):
        user = self.create_user(phone_number, email, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def normalize_phone_number(self, phone_number, pattern=r'^(\+989|09)+\d{9}$'):
        valid_phone = re.compile(pattern)
        if not valid_phone.match(phone_number):
            raise ValidationError("Phone number can be one of these forms: +989XXXXXXXXX | 09XXXXXXXXX")
        return phone_number
