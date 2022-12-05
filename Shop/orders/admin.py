from django.contrib import admin
from .models import Order, Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('discount', 'valid_since', 'valid_until', 'active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'paid')
    list_filter = ('paid', 'customer')
    search_fields = ('customer',)
