from django import forms
from django.utils.translation import gettext_lazy as _
from core.utils import phone_regex_validator


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=3, label='', initial=1,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ChooseAddressApplyCouponForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.order = kwargs.pop('order', None)
        super(ChooseAddressApplyCouponForm, self).__init__(*args, **kwargs)

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

        if self.order.coupon:
            self.fields['coupon'].initial = self.order.coupon.code

    address = forms.ModelChoiceField(queryset=None, label=_('Address'), initial=None,
                                     help_text=_(
                                         'If you have an address choose it from the list. Otherwise, add a new one'),
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    phone_number = forms.CharField(validators=[phone_regex_validator], label=_('Phone number'),
                                   help_text=_('Enter your phone number. Example: +989123456789'),
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    coupon = forms.CharField(required=False, label=_('Coupon'),
                             help_text=_('If you have coupon, You can enter it here'),
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
