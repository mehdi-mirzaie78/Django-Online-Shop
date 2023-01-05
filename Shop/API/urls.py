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
    path('address/update/<int:address_id>/', views.AddressUpdateAPIView.as_view(), name='api_address_update'),
    path('address/delete/<int:address_id>/', views.AddressDeleteAPIView.as_view(), name='api_address_delete'),
    # --------------------- product app ----------------------
    path('categories/', views.CategoryListAPIView.as_view(), name='api_categories_list'),
    path('products/', views.ProductListAPIView.as_view(), name='api_products_list'),
    path('product/<slug:slug>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('product/<slug:slug>/comment/create/', views.CommentCreateAPIView.as_view(), name='api_comment_create'),
    # --------------------- bucket -----------------------
    path('bucket/', views.BucketListAPIView.as_view(), name='api_bucket_list'),
    path('bucket/delete/<str:key>/', views.BucketDeleteAPIView.as_view(), name='api_bucket_delete'),
    path('bucket/download/<str:key>/', views.BucketDownloadAPIView.as_view(), name='api_bucket_download'),
    path('bucket/upload/<str:key>', views.BucketUploadAPIView.as_view(), name='api_bucket_upload'),
    # --------------------- orders app ------------------------
    path('cart/', views.CartAPIView.as_view(), name='api_cart'),
    path('cart/add/<int:product_id>/', views.CartAPIView.as_view(), name='api_cart_add'),
    path('cart/remove/<int:product_id>/', views.CartAPIView.as_view(), name='api_cart_remove'),
    path('order/create/', views.OrderCreateAPIView.as_view(), name='api_order_create'),
    path('order/checkout/<int:order_id>/', views.OrderCheckoutAPIView.as_view(), name='api_order_checkout'),
    path('order/save/<int:order_id>/', views.OrderSaveInfoAPIView.as_view(), name='api_order_save_info'),
    path('order/pay/<int:order_id>/', views.OrderPayAPIView.as_view(), name='api_order_pay'),

]
