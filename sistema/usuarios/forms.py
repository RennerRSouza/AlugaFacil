from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCadastroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'tipo_usuario', 'telefone']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'tipo_usuario': 'Tipo de Conta',
            'telefone': 'Telefone',
        }

class UsuarioEditarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefone']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'telefone': 'Telefone',
        }