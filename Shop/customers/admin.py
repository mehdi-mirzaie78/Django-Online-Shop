from django.contrib import admin
from .models import Customer, Address
from core.admin import BaseAdmin


class AddressInline(admin.TabularInline):
    model = Address


@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    ordering = ('user',)
    list_display = ('user',)
    search_fields = ('user_full_name', 'user_phone_number', 'user_email')

    fieldsets = (
        ('Personal Information', {'fields': ('user',)}),
        ('Optional', {'fields': ('image',)})
    )

    inlines = (AddressInline,)


@admin.register(Address)
class AddressAdmin(BaseAdmin):
    ordering = ('city',)
    list_display = ('customer', 'city', 'body', 'postal_code')
    list_editable = ('city', 'body')
    list_filter = ('city', 'body')

# admin.site.register(Customer, CustomerAdmin)
# admin.site.register(Address, AddressAdmin)
