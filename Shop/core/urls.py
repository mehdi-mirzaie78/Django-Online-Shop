from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
]
