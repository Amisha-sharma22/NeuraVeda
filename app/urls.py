from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get/', views.get_response, name='get_response'),
]