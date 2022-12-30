from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_details'),
    path('delete/<int:order_id>/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('payment/<int:order_id>/', views.PaymentView.as_view(), name='payment'),

    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),


]