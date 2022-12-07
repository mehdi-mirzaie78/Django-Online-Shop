from django.shortcuts import render
from django.views import View
from .models import Product


class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product/index.html', {'products': products})


class ProductDetailsView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        properties = product.properties.all()
        return render(request, 'product/details.html', {'product': product, 'properties': properties})
