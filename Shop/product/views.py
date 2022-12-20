from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Category
from .forms import ProductSearchForm, AddToCartForm, UploadForm
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin


class LandingPageView(View):
    def get(self, request):
        return render(request, 'product/landing.html')


class HomeView(View):
    form_class = ProductSearchForm

    def get(self, request, category_slug=None):
        products = Product.objects.get_active_list().all()  # gets all objects that are active
        if request.GET.get('search'):
            products = products.filter(name__contains=request.GET['search'])

        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'product/index.html',
                      {'products': products, 'categories': categories, 'form': self.form_class})


class ProductDetailsView(View):
    def get(self, request, slug):
        form = AddToCartForm
        product = Product.objects.get_active_list().get(slug=slug)
        properties = product.properties.all()
        return render(request, 'product/details.html', {'product': product, 'properties': properties, 'form': form})


class BucketView(IsAdminUserMixin, View):
    template_name = 'product/bucket.html'
    form_class = UploadForm

    def get(self, request):
        objects = tasks.all_objects_task()
        form = self.form_class
        return render(request, self.template_name, {'objects': objects, 'form': form})

    def post(self, request):
        objects = tasks.all_objects_task()
        form = self.form_class(files=request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            tasks.upload_object_task.delay(key=form.cleaned_data['file'].name)
            messages.success(request, 'Upload will be started soon', 'info')
            return redirect('product:bucket')
        messages.error(request, 'Something went wrong. Please try again', 'danger')
        return render(request, self.template_name, {'objects': objects, 'form': form})


class DeleteBucketObject(IsAdminUserMixin, View):

    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'your object will be deleted soon', 'info')
        return redirect('product:bucket')


class DownloadBucketObject(IsAdminUserMixin, View):

    def get(self, request, key):
        print(key, type(key))
        tasks.download_object_task.delay(key)
        messages.success(request, 'Download will be started soon', 'info')
        return redirect('product:bucket')
