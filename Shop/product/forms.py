from django import forms
from django.utils.translation import gettext_lazy as _


class ProductSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False, label='',
        widget=forms.TextInput(attrs={'class': 'form-control col-12 py-1', 'placeholder': _('Search')}))


class UploadForm(forms.Form):
    file = forms.FileField(label='', widget=forms.FileInput(attrs={'class': 'form-control'}))
