from django.db import models
from product.models import Product
from customers.models import Customer
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from core.models import BaseModel
from django.utils import timezone


class Coupon(BaseModel):
    code = models.CharField(max_length=30, unique=True)
    valid_since = models.DateTimeField()
    valid_until = models.DateTimeField()
    discount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])

    def __str__(self):
        return self.code

    def is_coupon_valid(self):
        now = timezone.now()
        if self.valid_until < now or self.valid_since > now:
            return False
        return True


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE, related_name='coupon_order', null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(blank=True, null=True, default=0, editable=False)
    city = models.CharField(max_length=20, default='Not specified')
    body = models.CharField(max_length=120, default='Not specified')
    postal_code = models.CharField(
        max_length=10,
        default='XXXXXXXXXX',
        validators=[RegexValidator(r'\d{10}', message='Invalid Postal code')])
    STATUS = [('pending', 'PENDING'), ('checking', 'CHECKING'), ('sending', 'SENDING'), ('done', 'DONE')]
    status = models.CharField(max_length=30, choices=STATUS, default='PENDING')
    transaction_code = models.CharField(max_length=20, null=True, editable=False)

    class Meta:
        ordering = ('is_paid', '-updated')

    def __str__(self):
        return f'{self.customer} - {self.id}'

    def apply_coupon(self):
        self.discount = self.coupon.discount if self.coupon else 0

    def get_total_price(self, code):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = total * self.discount / 100
            return int(total - discount_price)
        return total


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    STATUS = [('ok', 'OK'), ('no', 'NO'), ('supplying', 'SUPPLYING')]
    status = models.CharField(max_length=30, choices=STATUS, default='OK')

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def check_status(self):
        return True if self.status == 'OK' else False


