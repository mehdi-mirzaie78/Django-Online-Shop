from django import forms
from django.utils.translation import gettext_lazy as _

from product.models import Comment


class ProductSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False, label='',
        widget=forms.TextInput(attrs={'class': 'form-control col-12 py-1', 'placeholder': _('Search')}))


class UploadForm(forms.Form):
    file = forms.FileField(label='', widget=forms.FileInput(attrs={'class': 'form-control'}))


class AddCommentForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=True, label=_('Title'))
    comment = forms.CharField(required=True, label=_('Comment'), widget=forms.Textarea(attrs={'rows': 5}))
