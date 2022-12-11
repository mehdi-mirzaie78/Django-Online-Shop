from django.contrib import admin
from .models import Product, Category, Comment, Property
from core.admin import BaseAdmin


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('name', 'sub_category', 'is_sub', 'created', 'updated', 'is_deleted')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Property)
class PropertyAdmin(BaseAdmin):
    list_display = ('key', 'value', 'created', 'updated', 'is_deleted')
    list_filter = ('key', 'value')


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = (
        'name', 'price_no_discount', 'discount', 'stock', 'is_available', 'created', 'updated', 'is_deleted',
        'is_active')
    list_filter = ('category', 'name', 'price', 'stock',)
    search_fields = ('name',)
    ordering = ('is_deleted', 'name')
    fieldsets = (
        ('Product Information',
         {'fields': (
             'name', 'slug', 'category', 'property', 'image_tag', 'image', 'description', 'price_no_discount',
             'discount', 'price',
             'stock', 'is_available',)}
         ),
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_tag', 'price', 'is_available',)
    list_per_page = 10
    # list_editable = ('stock', 'price_no_discount', 'discount')

    filter_horizontal = ('category', 'properties',)


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    list_display = ('customer', 'product', 'title', 'created', 'updated', 'is_deleted', 'is_active')
    list_filter = ('customer', 'product')
    search_fields = ('customer', 'product')
    list_per_page = 10
