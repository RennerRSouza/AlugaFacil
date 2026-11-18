from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UsuarioCadastroForm

def cadastro(request):
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo(a), {usuario.username}.')
            return redirect('imoveis:home')
    else:
        form = UsuarioCadastroForm()
    
    return render(request, 'usuarios/cadastro.html', {'form': form})