from django.contrib import admin
from .models import Customer, Address
from core.admin import BaseAdmin


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    ordering = ('user',)
    list_display = ('user', 'user_full_name', 'phone_number')
    search_fields = ('user__full_name', 'user__phone_number')

    fieldsets = (
        ('Personal Information', {'fields': ('user', 'gender', 'age',)}),
        ('Optional', {'fields': ('image_tag', 'image')}),
    )

    readonly_fields = ('image_tag',)
    inlines = (AddressInline,)
    list_per_page = 10


@admin.register(Address)
class AddressAdmin(BaseAdmin):
    ordering = ('city',)
    list_display = ('customer', 'city', 'postal_code')
    list_filter = ('city', 'body')
    search_fields = ('customer', 'city', 'body')
