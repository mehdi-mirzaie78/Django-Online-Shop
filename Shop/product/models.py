from django.db import models
from customers.models import Customer
from core.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.html import mark_safe
from django.urls import reverse


class Category(BaseModel):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('is_sub', 'name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:category_filter', args=(self.slug,))


class Property(BaseModel):
    key = models.CharField(max_length=120)
    value = models.CharField(max_length=255, unique=True)
    priority = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'property'
        verbose_name_plural = 'properties'
        ordering = ('priority',)

    def __str__(self):
        return f'{self.key}:{self.value}'


class Product(BaseModel):
    category = models.ManyToManyField(Category, related_name='products')
    properties = models.ManyToManyField(Property, related_name='p_products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/', default='default/product.png', null=True, blank=True)
    description = models.TextField()
    price_no_discount = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(90)])
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ccomments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments')
    title = models.CharField(max_length=120)
    body = models.TextField()

    def __str__(self):
        return f'{self.customer} commented on {self.product}'
