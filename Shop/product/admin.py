from django.contrib import admin
from .models import Product, Category, Comment

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)
    list_display = ('name', 'price', 'stock', 'is_available')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'title')
    list_filter = ('customer', 'product')
    search_fields = ('customer', 'product')