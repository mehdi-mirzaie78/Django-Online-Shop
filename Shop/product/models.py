from django.db import models
from customers.models import Customer


class Category(models.Model):
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


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def is_available(self):
        return True if self.stock > 0 else False

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ccomments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments')
    title = models.CharField(max_length=120)
    body = models.TextField()

    def __str__(self):
        return f'{self.customer} commented on {self.product}'
