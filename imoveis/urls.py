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
    path('imovel/<int:pk>/favoritar/', views.toggle_favorito, name='toggle_favorito'),
    path('imovel/<int:pk>/interesse/', views.demonstrar_interesse, name='demonstrar_interesse'),
    path('imovel/<int:pk>/status/', views.alterar_status_imovel, name='alterar_status_imovel'),
    path('interesse/<int:pk>/responder/', views.responder_interesse, name='responder_interesse'),
    path('interesse/<int:pk>/cancelar/', views.cancelar_interesse, name='cancelar_interesse'),
    path('painel/usuario/<int:pk>/excluir/', views.admin_excluir_usuario, name='admin_excluir_usuario'),
    path('imovel/foto/<int:pk>/excluir/', views.excluir_foto_imovel, name='excluir_foto_imovel'),
]