from django import forms
from django.utils.translation import gettext_lazy as _
from core.utils import phone_regex_validator


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=3, label='', initial=1,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ChooseAddressForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.order = kwargs.pop('order', None)
        super(ChooseAddressForm, self).__init__(*args, **kwargs)

        self.customer = self.request.user.customer
        queryset = self.customer.addresses.all()
        self.fields['address'].queryset = queryset
        order_address = queryset.filter(postal_code=self.order.postal_code)

        if order_address.exists():
            self.fields['address'].initial = order_address.get()

        if self.order.phone_number:
            self.fields['phone_number'].initial = self.order.phone_number
        else:
            self.fields['phone_number'].initial = self.customer.user.phone_number
    address = forms.ModelChoiceField(queryset=None, label=_('Address'), initial=None,
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   validators=[phone_regex_validator])
