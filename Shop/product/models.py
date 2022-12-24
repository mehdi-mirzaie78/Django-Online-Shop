from django.db import models
from customers.models import Customer
from core.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.html import mark_safe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(BaseModel):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True,
                                     verbose_name=_('Upper Category'))
    is_sub = models.BooleanField(default=False, verbose_name=_('Sub Category Status'))
    name = models.CharField(max_length=200, verbose_name=_('Category Name'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('Slug'))

    class Meta:
        ordering = ('is_sub', 'name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:category_filter', args=(self.slug,))


class Property(BaseModel):
    key = models.CharField(max_length=120, verbose_name=_('Property Key'))
    value = models.CharField(max_length=255, unique=True, verbose_name=_('Property Value'))
    priority = models.IntegerField(default=1, verbose_name=_('Priority'))

    class Meta:
        verbose_name = _('property')
        verbose_name_plural = _('properties')
        ordering = ('priority',)

    def __str__(self):
        return f'{self.key}:{self.value}'


class Product(BaseModel):
    category = models.ManyToManyField(Category, related_name='products', verbose_name=_('Category'))
    properties = models.ManyToManyField(Property, related_name='p_products', verbose_name=_('Properties'))
    name = models.CharField(max_length=200, verbose_name=_('Product Name'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('Slug'))
    image = models.ImageField(default='product.png', null=True, blank=True, verbose_name=_('Image'))
    description = models.TextField(verbose_name=_('Description'))
    price_no_discount = models.PositiveIntegerField(verbose_name=_('Price without discount'))
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(90)], verbose_name=_('Discount'))
    price = models.PositiveIntegerField(verbose_name=_('Price'))
    stock = models.PositiveIntegerField(verbose_name=_('Stock'))
    is_available = models.BooleanField(null=True, blank=True, verbose_name=_('Availability Status'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def save(self, *args, **kwargs):
        self.is_available = True if self.stock > 0 else False
        self.price = self.price_no_discount - self.discount * self.price_no_discount / 100
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="250" height="250" />')

    image_tag.short_description = 'Image'


class Comment(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ccomments', verbose_name=_('Customer'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments', verbose_name=_('Product'))
    title = models.CharField(max_length=120, verbose_name=_('Title'))
    body = models.TextField(verbose_name=_('Body'))

    def __str__(self):
        return f'{self.customer} commented on {self.product}'
