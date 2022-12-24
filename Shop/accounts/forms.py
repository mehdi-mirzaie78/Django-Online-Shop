from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator
from customers.models import Customer
from core.utils import phone_regex_validator, full_name_regex_validator
from django.utils.translation import gettext_lazy as _


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('Passwords don\'t match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="You can change password using <a href=\"../password/\">this form</a>")

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'last_login']
        labels = {'email': _('email'), 'phone_number': _('phone_number'),
                  'full_name': _('password'), 'last_login': _('last_login')}


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label=_('Full name'), widget=forms.TextInput(attrs={'class': 'form-control'}),
                                validators=[full_name_regex_validator])
    phone = forms.CharField(
        label=_('Phone Number'),
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[phone_regex_validator]
    )
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError('This email already exists')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone)
        if user.exists():
            raise ValidationError('This phone number already exists')
        return phone


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(label=_('Code'), widget=forms.NumberInput(attrs={'class': 'form-control'}))


class UserLoginForm(forms.Form):
    phone = forms.CharField(
        label=_('Phone'),
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(
            regex=r'^(\+989|09)+\d{9}$',
            message="Invalid Phone number. Phone number must be like: +989XXXXXXXXX or 09XXXXXXXXX")]
    )
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(label=_('Full Name'), widget=forms.TextInput(attrs={'class': 'form-control'}),
                                validators=[full_name_regex_validator])
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label=_('Phone Number'), widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   validators=[phone_regex_validator])

    class Meta:
        model = Customer
        fields = ('image', 'gender', 'age')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'image': _('image'), 'gender': _('gender'), 'age': _('age')
                  }
