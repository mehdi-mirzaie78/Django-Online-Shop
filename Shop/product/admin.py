from django.contrib import admin
from .models import Product, Category, Comment, Property
from core.admin import BaseAdmin


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('name', 'sub_category', 'is_sub')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Property)
class PropertyAdmin(BaseAdmin):
    raw_id_fields = ('product',)
    list_display = ('key', 'value')
    list_filter = ('key', 'value')


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)
    list_display = ('name', 'price', 'stock', 'is_available')
    list_filter = ('name', 'price', 'stock',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    list_display = ('customer', 'product', 'title')
    list_filter = ('customer', 'product')
    search_fields = ('customer', 'product')
