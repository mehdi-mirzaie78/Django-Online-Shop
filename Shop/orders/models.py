from django.db import models
from product.models import Product
from customers.models import Customer, Address
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from core.models import BaseModel
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.utils import phone_regex_validator


class Coupon(BaseModel):
    code = models.CharField(max_length=30, unique=True, verbose_name=_("Coupon Code"))
    valid_since = models.DateTimeField(verbose_name=_("Valid Since"))
    valid_until = models.DateTimeField(verbose_name=_("Valid Until"))
    discount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)],
                                           verbose_name=_("Discount"))

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    def __str__(self):
        return self.code

    def is_coupon_valid(self):
        now = timezone.now().replace(tzinfo=timezone.utc)
        if self.valid_since < now < self.valid_until:
            return True
        return False


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name=_("Customer"))
    coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE, related_name='coupon_order', null=True, blank=True,
                                  verbose_name=_("Coupon"))
    is_paid = models.BooleanField(default=False, verbose_name=_("Payment Status"))
    discount = models.PositiveIntegerField(blank=True, null=True, default=0, editable=False, verbose_name=_("Discount"))

    # city and body is for address fields
    city = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("City"))
    body = models.CharField(max_length=120, null=True, blank=True, verbose_name=_("Address"))
    postal_code = models.CharField(
        max_length=10, null=True, blank=True,
        validators=[RegexValidator(r'\d{10}', message='Invalid Postal code')],
        verbose_name=_("Postal Code"))
    phone_number = models.CharField(max_length=13, null=True, blank=True, validators=[phone_regex_validator])
    STATUS = [(_('PENDING'), _('PENDING')), (_('CHECKING'), _('CHECKING')), (_('SENDING'), _('SENDING')),
              (_('DONE'), _('DONE'))]
    status = models.CharField(max_length=30, choices=STATUS, default='PENDING', verbose_name=_("Status"))
    transaction_code = models.CharField(max_length=20, null=True, editable=False, verbose_name=_("Transaction Code"))

    class Meta:
        ordering = ('is_paid', '-updated')
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'Order: {self.id} - {self.updated.date()} - {self.status}'

    def save(self, *args, **kwargs):
        if self.coupon and self.coupon.is_coupon_valid():
            self.apply_coupon()
        else:
            self.coupon = None
            self.discount = 0
        super().save(*args, **kwargs)

    def apply_coupon(self):
        self.discount = self.coupon.discount if self.coupon else 0

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = total * self.discount / 100
            return int(total - discount_price)
        return total

    def check_address(self):
        return True if self.customer.addresses else False

    def save_address(self, address, phone_number):
        self.city, self.body, self.postal_code = address.city, address.body, address.postal_code
        self.phone_number = phone_number
        self.save()


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_("Order"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    price = models.PositiveIntegerField(verbose_name=_("Price"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))
    STATUS = [('ok', _('OK')), ('no', _('NO')), ('supplying', _('SUPPLYING'))]
    status = models.CharField(max_length=30, choices=STATUS, default='OK', verbose_name=_("Status"))

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def check_status(self):
        return True if self.status == 'OK' else False
