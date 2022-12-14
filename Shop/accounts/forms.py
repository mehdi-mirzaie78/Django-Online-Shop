from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator
from customers.models import Customer


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

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


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='Full name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(
            regex=r'^(\+989|09)+\d{9}$',
            message="Invalid Phone number. Phone number must be like: +989XXXXXXXXX or 09XXXXXXXXX")]
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError('This email already exists')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = '0' + phone[3:] if len(phone) == 13 else phone
        user = User.objects.filter(phone_number=phone)
        if user.exists():
            raise ValidationError('This phone number already exists')
        return phone


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


class UserLoginForm(forms.Form):
    phone = forms.CharField(
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(
            regex=r'^(\+989|09)+\d{9}$',
            message="Invalid Phone number. Phone number must be like: +989XXXXXXXXX or 09XXXXXXXXX")]
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ('image', 'gender', 'age')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }
