from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UsuarioCadastroForm, UsuarioEditarForm

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

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:editar_perfil')
    else:
        form = UsuarioEditarForm(instance=request.user)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})

@login_required
def excluir_conta(request):
    if request.user.is_superuser:
        messages.warning(request, 'Contas de superusuário não podem ser excluídas por esta tela.')
        return redirect('usuarios:editar_perfil')

    if request.method == 'POST':
        usuario = request.user
        logout(request)
        usuario.delete()
        messages.success(request, 'Sua conta e todos os seus dados foram excluídos.')
        return redirect('imoveis:home')

    return render(request, 'usuarios/excluir_conta.html', {'usuario_alvo': request.user})