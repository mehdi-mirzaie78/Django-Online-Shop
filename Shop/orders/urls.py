from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    # Orders
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('udpate/<int:order_id>/', views.OrderUpdateView.as_view(), name='order_update'),
    path('details/<int:order_id>/', views.OrderDetailView.as_view(), name='order_details'),
    path('delete/<int:order_id>/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('payment/<int:order_id>/', views.OrderPaymentView.as_view(), name='payment'),
    path('verify/', views.OrderVerifyView.as_view(), name='order_verify'),
    # Shopping Cart
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),

]
