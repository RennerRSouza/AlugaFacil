from django.urls import path
from .views import *
from . import views

app_name = 'imoveis'

urlpatterns = [
    path('', views.home, name='home'),
    path('imovel/<int:pk>/', views.detalhes, name='detalhes'),
]