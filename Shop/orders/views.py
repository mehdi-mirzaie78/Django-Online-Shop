from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .cart import Cart
from product.models import Product
from .forms import AddToCartForm, ChooseAddressForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from customers.models import Customer, Address


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

        return redirect('orders:order_details', order.id)


class OrderDetailView(LoginRequiredMixin, View):
    form_class = ChooseAddressForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if address_id := request.GET.get('address_id', None):
            address = get_object_or_404(Address, id=address_id)
            order.city = address.city
            order.body = address.body
            order.postal_code = address.postal_code
            order.save()

        if order.check_address():
            return render(request, 'orders/order.html', {'order': order, 'form': self.form_class(request=request)})
        return redirect('orders:address_create')



