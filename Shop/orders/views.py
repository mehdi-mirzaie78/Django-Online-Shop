from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .cart import Cart
from product.models import Product
from .forms import AddToCartForm, ChooseAddressForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from customers.models import Customer, Address
from django.utils.translation import gettext_lazy as _


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        customer = get_object_or_404(Customer, user=request.user)
        order = Order.objects.create(customer=customer)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
            )
        cart.clear()
        return redirect('orders:order_details', order.id)


class OrderDetailView(LoginRequiredMixin, View):
    form_class = ChooseAddressForm
    template_name = 'orders/order_details.html'

    def setup(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, id=kwargs['order_id'])
        return super(OrderDetailView, self).setup(request, *args, **kwargs)

    def get(self, request, order_id):
        order = self.order
        form = self.form_class(request=request, order=order)
        if order.check_address():
            return render(request, self.template_name, {'order': order, 'form': form})
        return redirect('customers:address_create')

    def post(self, request, order_id):
        order = self.order
        form = self.form_class(request.POST, request=request, order=order)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']

            order.city = address.city
            order.body = address.body
            order.postal_code = address.postal_code
            order.phone_number = phone_number
            order.save()
            return redirect('orders:order_details', order.id)
        return render(request, self.template_name, {'order': order, 'form': form})


class OrderDeleteView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, _('Order deleted successfully'), 'info')
        return redirect('accounts:user_profile')


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.is_paid = True
        order.save()
        return redirect('accounts:user_profile')
