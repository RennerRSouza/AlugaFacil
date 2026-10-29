from django.urls import path
from .views import *
from . import views

app_name = 'imoveis'

urlpatterns = [
    path('', views.home, name='home'),
    path('imovel/<int:pk>/', views.detalhes, name='detalhes'),
    path('imovel/novo/', views.novo_imovel, name='novo_imovel'),
    path('painel/', views.meu_painel, name='meu_painel'),
    path('imovel/<int:pk>/editar/', views.editar_imovel, name='editar_imovel'),
    path('imovel/<int:pk>/excluir/', views.excluir_imovel, name='excluir_imovel'),
]