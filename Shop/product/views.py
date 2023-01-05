from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Category, Comment
from .forms import ProductSearchForm, UploadForm, AddCommentForm
from orders.forms import AddToCartForm
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class LandingPageView(View):
    def get(self, request):
        return render(request, 'product/landing.html')


class HomeView(View):
    form_class = ProductSearchForm

    def get(self, request, category_slug=None):
        products = Product.objects.get_active_list().all()  # gets all objects that are active
        if request.GET.get('search'):
            products = products.filter(name__contains=request.GET['search'])

        categories = Category.objects.get_active_list().filter(is_sub=False)
        if category_slug:
            category = Category.objects.get_active_list().get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'product/index.html',
                      {'products': products, 'categories': categories, 'form': self.form_class})


class ProductDetailsView(View):
    form_add = AddToCartForm
    form_comment = AddCommentForm
    template_name = 'product/details.html'

    def setup(self, request, *args, **kwargs):
        self.product = Product.objects.get_active_list().get(slug=kwargs['slug'])
        self.properties = self.product.properties.all()
        self.comments = self.product.pcomments.all()
        return super().setup(request, *args, **kwargs)

    def get(self, request, slug):
        product = self.product
        properties = self.properties
        comments = self.comments
        return render(request, self.template_name, {'product': product, 'properties': properties, 'form': self.form_add,
                                                    'form_comment': self.form_comment, 'comments': comments})

    @method_decorator(login_required)
    def post(self, request, slug):
        form_comment = self.form_comment(request.POST)
        if form_comment.is_valid():
            cd = form_comment.cleaned_data
            comment = Comment.objects.create(
                customer=request.user.customer,
                product=self.product,
                title=cd['title'],
                body=cd['comment'],
            )
            messages.success(request, _('Comment added successfully'), 'info')
            return redirect('product:product_details', slug=slug)
        messages.error(request, _('Something went wrong. Check the possible errors'), 'danger')
        return render(request, self.template_name, {'form_comment': form_comment, 'product': self.product,
                                                    'properties': self.properties, 'comments': self.comments})


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
            messages.success(request, _('Upload will be started soon'), 'info')
            return redirect('product:bucket')
        messages.error(request, _('Something went wrong. Please try again'), 'danger')
        return render(request, self.template_name, {'objects': objects, 'form': form})


class DeleteBucketObject(IsAdminUserMixin, View):

    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, _('your object will be deleted soon'), 'info')
        return redirect('product:bucket')


class DownloadBucketObject(IsAdminUserMixin, View):

    def get(self, request, key):
        print(key, type(key))
        tasks.download_object_task.delay(key)
        messages.success(request, _('Download will be started soon'), 'info')
        return redirect('product:bucket')
