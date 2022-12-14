from django import forms


class ProductSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False, label='',
        widget=forms.TextInput(attrs={'class': 'form-control col-12 py-1', 'placeholder': 'Search'}))
