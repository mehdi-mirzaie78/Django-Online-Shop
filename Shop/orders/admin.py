from django.contrib import admin
from .models import Order, OrderItem, Coupon
from core.admin import BaseAdmin


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Coupon)
class CouponAdmin(BaseAdmin):
    list_display = ('discount', 'valid_since', 'valid_until', 'active')


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ('id', 'customer', 'paid')
    list_filter = ('paid', 'customer')
    search_fields = ('customer',)
    inlines = (OrderItemInline,)
