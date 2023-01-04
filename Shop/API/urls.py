from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
    # --------------------- accounts app ---------------------
    path('profile/', views.ProfileAPIView.as_view(), name='api_profile'),
    path('profile/update/', views.ProfileUpdateAPIView.as_view(), name='api_profile_update'),
    # --------------------- customers app --------------------
    path('addresses/', views.AddressListAPIView.as_view(), name='api_addresses_list'),
    path('address/create/', views.AddressCreateAPIView.as_view(), name='api_address_create'),
    # --------------------- product app ----------------------
    path('categories/', views.CategoryListAPIView.as_view(), name='api_categories_list'),
    path('products/', views.ProductListAPIView.as_view(), name='api_products_list'),
    path('product/<slug:slug>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('bucket/', views.BucketListAPIView.as_view(), name='api_bucket_list'),
    path('bucket/delete/<str:key>/', views.BucketDeleteAPIView.as_view(), name='api_bucket_delete'),
    path('bucket/download/<str:key>/', views.BucketDownloadAPIView.as_view(), name='api_bucket_download'),
    path('bucket/upload/<str:key>', views.BucketUploadAPIView.as_view(), name='api_bucket_upload'),
    # --------------------- order app ------------------------
    path('cart/', views.CartAPIView.as_view(), name='api_cart'),
    path('cart/add/<int:product_id>/', views.CartAPIView.as_view(), name='api_cart_add'),
    path('cart/remove/<int:product_id>/', views.CartAPIView.as_view(), name='api_cart_remove')
]
