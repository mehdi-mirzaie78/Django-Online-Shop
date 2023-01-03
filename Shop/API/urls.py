from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
    path('profile/', views.ProfileAPIView.as_view(), name='api_profile'),
    path('profile/update/', views.ProfileUpdateAPIView.as_view(), name='api_profile_update'),
    path('addresses/', views.AddressListAPIView.as_view(), name='api_addresses_list'),
    path('address/create/', views.AddressCreateAPIView.as_view(), name='api_address_create'),


]
