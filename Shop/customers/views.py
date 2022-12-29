from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import AddressAddForm, AddressUpdateForm
from .models import Address
from django.utils.translation import gettext_lazy as _


class AddressCreateView(LoginRequiredMixin, View):
    form_class = AddressAddForm
    template_name = 'customers/address_create.html'

    def get(self, request):
        form = self.form_class
        customer = request.user.customer
        # addresses = customer.addresses.all()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Address.objects.create(
                customer=self.request.user.customer,
                city=cd['city'],
                body=cd['body'],
                postal_code=cd['postal_code'],
            )
            messages.success(request, _('New address added to your address list.'), 'success')
            return redirect('accounts:user_profile')
        messages.error(request, _('Something went wrong please try again.'), 'danger')
        return render(request, self.template_name, {'form': form})


class AddressUpdateView(LoginRequiredMixin, View):
    template_name = 'customers/address_update.html'
    form_class = AddressUpdateForm

    def setup(self, request, *args, **kwargs):
        self.address = get_object_or_404(Address, id=kwargs['address_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, address_id):
        form = self.form_class(instance=self.address)
        return render(request, self.template_name, {'form': form})

    def post(self, request, address_id):
        form = self.form_class(request.POST, instance=self.address)
        if form.is_valid():
            form.save()
            messages.success(request, _('Address updated successfully'), 'success')
            return redirect('accounts:user_profile')

        messages.error(request, _('Something went wrong. Please try again.'), 'error')
        return render(request, self.template_name, {'form': form})


class AddressDeleteView(View):
    def get(self, request, address_id):
        address = get_object_or_404(Address, id=address_id)
        address.delete()
        messages.success(request, _('Address deleted successfully'), 'success')
        return redirect('accounts:user_profile')