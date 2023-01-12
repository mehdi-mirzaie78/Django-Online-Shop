from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    path('address/create/', views.AddressCreateView.as_view(), name='address_create'),
    path('address/update/<int:address_id>', views.AddressUpdateView.as_view(), name='address_update'),
    path('address/delete/<int:address_id>', views.AddressDeleteView.as_view(), name='address_delete'),
]