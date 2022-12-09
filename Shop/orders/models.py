from django.db import models
from product.models import Product
from customers.models import Customer
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models import BaseModel


class Receipt(BaseModel):
    order_details = models.TextField(default='No information')

    def __str__(self):
        return self.order_details[:120]


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(blank=True, null=True, default=None)
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE, related_name='rorder', null=True, blank=True)

    class Meta:
        ordering = ('paid', '-updated')

    def __str__(self):
        return f'{self.customer} - {self.id}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = total * self.discount / 100
            return int(total - discount_price)
        return total

    def get_details(self):
        items = self.items.all()
        result = ''
        for item in items:
            result += item.get_item_details() + '\n'
        return result

    def create_receipt(self):
        if self.paid:
            self.receipt = Receipt.objects.create(order_details=self.get_details())
            print(self.receipt.order_details)
            return self.receipt.id
        return False


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_item_details(self):
        detail = f'{self.product}|{self.quantity}|{self.price}|{self.get_cost()}'
        return detail


class Coupon(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='used_coupon')
    code = models.CharField(max_length=30, unique=True)
    valid_since = models.DateTimeField()
    valid_until = models.DateTimeField()
    discount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
