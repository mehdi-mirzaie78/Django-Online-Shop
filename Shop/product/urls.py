from django.urls import path, include
from . import views

app_name = 'product'

bucket_urls = [
    path('', views.BucketView.as_view(), name='bucket'),
    path('delete_obj/<str:key>/', views.DeleteBucketObject.as_view(), name='delete_obj_bucket'),
    path('download_obj/<str:key>/', views.DownloadBucketObject.as_view(), name='download_obj_bucket'),
]

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('bucket/', include(bucket_urls)),
    path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category_filter'),
    path('details/<slug:slug>/', views.ProductDetailsView.as_view(), name='product_details'),
]
