from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Imovel
from .forms import ImovelForm

def home(request):
    imoveis_lista = Imovel.objects.filter(status='DISPONIVEL').order_by('-data_cadastro')
    context = {
        'imoveis': imoveis_lista
    }  
    return render(request, 'imoveis/home.html', context)

def detalhes(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)   
    return render(request, 'imoveis/detalhes.html', {'imovel': imovel})

@login_required 
def novo_imovel(request):
    if request.user.tipo_usuario != 'PROPRIETARIO':
        return redirect('imoveis:home')

    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES)
        if form.is_valid():
            imovel = form.save(commit=False)
            imovel.proprietario = request.user
            imovel.save()
            return redirect('imoveis:home')
    else:
        form = ImovelForm()
        
    return render(request, 'imoveis/novo_imovel.html', {'form': form})

@login_required
def meu_painel(request):
    if request.user.tipo_usuario == 'PROPRIETARIO':
        meus_imoveis = Imovel.objects.filter(proprietario=request.user).order_by('-data_cadastro')
        return render(request, 'imoveis/painel_proprietario.html', {'imoveis': meus_imoveis})
    
    else:
        return render(request, 'imoveis/painel_inquilino.html')

@login_required
def editar_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk, proprietario=request.user)
    
    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES, instance=imovel)
        if form.is_valid():
            form.save()
            return redirect('imoveis:meu_painel')
    else:
        form = ImovelForm(instance=imovel)
        
    return render(request, 'imoveis/novo_imovel.html', {'form': form, 'editando': True})

@login_required
def excluir_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk, proprietario=request.user)
    
    if request.method == 'POST':
        imovel.delete()
        return redirect('imoveis:meu_painel')
        
    return render(request, 'imoveis/excluir_imovel.html', {'imovel': imovel})