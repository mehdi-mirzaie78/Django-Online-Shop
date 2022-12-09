from django.db import models
from customers.models import Customer
from core.models import BaseModel


class Category(BaseModel):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(BaseModel):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    @property
    def is_available(self):
        return True if self.stock > 0 else False

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ccomments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments')
    title = models.CharField(max_length=120)
    body = models.TextField()

    def __str__(self):
        return f'{self.customer} commented on {self.product}'


class Property(BaseModel):
    product = models.ManyToManyField(Product, related_name='properties')
    key = models.CharField(max_length=120)
    value = models.CharField(max_length=255)
    priority = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'property'
        verbose_name_plural = 'properties'
        ordering = ('priority',)

    def __str__(self):
        return f'{self.key}:{self.value}'
