from django.contrib import admin
from .models import Product, Category, Comment, Property


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    raw_id_fields = ('product',)
    list_display = ('key', 'value')
    list_filter = ('key', 'value')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)
    list_display = ('name', 'price', 'stock', 'is_available')
    list_filter = ('name', 'price', 'stock',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'title')
    list_filter = ('customer', 'product')
    search_fields = ('customer', 'product')
