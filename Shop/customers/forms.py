from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import Address


class AddressAddForm(forms.Form):
    city = forms.CharField(label=_('City'))
    body = forms.CharField(widget=forms.Textarea(), label=_('Address'))
    postal_code = forms.CharField(max_length=10, validators=[RegexValidator(regex=r'\d{10}', message=_(
        'Postal code must be a 10 digit number.'
    ))], label=_('Postal Code'))

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if Address.objects.filter(postal_code=postal_code).exists():
            raise forms.ValidationError(_('Postal code already exists.'))
        return postal_code


class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['customer']

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if Address.objects.filter(postal_code=postal_code).exists():
            raise forms.ValidationError(_('Postal code already exists.'))
        return postal_code
