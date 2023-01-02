from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
    path('profile/', views.ProfileAPIView.as_view(), name='api_profile')
]
