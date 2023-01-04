from django.contrib import admin
from .models import Order, OrderItem, Coupon
from core.admin import BaseAdmin

admin.site.register(OrderItem)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
    readonly_fields = ('price',)
    extra = 0


@admin.register(Coupon)
class CouponAdmin(BaseAdmin):
    list_display = ('discount', 'valid_since', 'valid_until', 'is_active')


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ('id', 'customer', 'is_paid')
    list_filter = ('is_paid', 'customer')
    search_fields = ('customer',)
    inlines = (OrderItemInline,)
    readonly_fields = ('city', 'body', 'postal_code', 'discount')
