from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),
    path('perfil/excluir/', views.excluir_conta, name='excluir_conta'),
]