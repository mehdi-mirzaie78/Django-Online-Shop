from django import forms
from django.utils.translation import gettext_lazy as _


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=3, label='', initial=1,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ChooseAddressForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChooseAddressForm, self).__init__(*args, **kwargs)
        self.customer = self.request.user.customer
        queryset = self.customer.addresses.all()
        self.fields['address_id'].queryset = queryset
        self.fields['address_id'].initial = queryset.first()

    address_id = forms.ModelChoiceField(queryset=None, label=_('Address'), initial=None,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
