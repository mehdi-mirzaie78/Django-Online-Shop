from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .cart import Cart
from product.models import Product
from .forms import AddToCartForm, ChooseAddressForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from customers.models import Customer
from django.utils.translation import gettext_lazy as _
from product.models import Product


class CartView(View):
    def get(self, request):
        customer = request.user.customer
        unpaid_orders = customer.orders.filter(is_paid=False)
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart, 'unpaid_orders': unpaid_orders})


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


class OrderUpdateView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        customer = get_object_or_404(Customer, user=request.user)
        order = Order.objects.filter(customer=customer, id=order_id)

        order = order.get()
        cart = Cart(request)

        order_items = OrderItem.objects.filter(order=order)

        for item in cart:
            # if item is not in order_items create an order_item for it
            if not order_items.filter(product=item['product']).exists():
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )

            # if item of cart in order_items: Update the quantity of the order_item
            elif order_items.filter(product=item['product']).exists():
                order_item = order_items.get(product=item['product'])
                order_item.quantity = item['quantity']
                order_item.save()

        # if there is an order_item which is not in cart items remove order_item
        for orderitem in order_items:
            product = orderitem.product
            if str(product.id) not in cart.cart:
                orderitem.delete()

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
            order.save_address(address, phone_number)
            messages.success(request, _('Address saved successfully'))
            return redirect('orders:order_details', order.id)
        messages.error(request, _('Please correct the error below.', 'danger'))
        return render(request, self.template_name, {'order': order, 'form': form})


class OrderDeleteView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, _('Order deleted successfully'), 'info')
        return redirect('orders:cart')


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        # TODO: Implement payment
        order.is_paid = True
        order.save()

        items = order.items.all()
        for item in items:
            product = Product.objects.get(id=item.product.id)
            product.stock -= item.quantity
            product.save()

        return redirect('accounts:user_profile')
