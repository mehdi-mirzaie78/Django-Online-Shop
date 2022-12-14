from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category_filter'),
    path('details/<slug:slug>/', views.ProductDetailsView.as_view(), name='product_details'),
]
