from django import forms


class ProductSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False, label='',
        widget=forms.TextInput(attrs={'class': 'form-control col-12 py-1', 'placeholder': 'Search'}))


class AddToCartForm(forms.Form):
    number = forms.IntegerField(min_value=1, max_value=3, label='',
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
