from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home')
]
