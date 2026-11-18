from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from httpx import request
from .models import Imovel, Favorito, Interesse
from .forms import ImovelForm, InteresseForm

def home(request):
    imoveis = Imovel.objects.filter(status='DISPONIVEL').order_by('-data_cadastro')

    cidade = request.GET.get('cidade')
    tipo = request.GET.get('tipo')
    quartos = request.GET.get('quartos')
    preco_max = request.GET.get('preco_max')

    if cidade:
        imoveis = imoveis.filter(cidade__icontains=cidade)
    if tipo:
        imoveis = imoveis.filter(tipo=tipo)
    if quartos:
        imoveis = imoveis.filter(quartos__gte=quartos)
    if preco_max:
        imoveis = imoveis.filter(preco_aluguel__lte=preco_max)

    context = {
        'imoveis': imoveis,
        'tipos_imovel': Imovel.TipoImovel.choices,
        'filtros': {
            'cidade': cidade or '',
            'tipo': tipo or '',
            'quartos': quartos or '',
            'preco_max': preco_max or '',
        }
    }
    
    return render(request, 'imoveis/home.html', context)

def detalhes(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)
    is_favorito = False
    interesse_existente = None
    
    if request.user.is_authenticated and request.user.tipo_usuario == 'INQUILINO':
        is_favorito = Favorito.objects.filter(usuario=request.user, imovel=imovel).exists()
        interesse_existente = Interesse.objects.filter(usuario=request.user, imovel=imovel).first()
        
    return render(request, 'imoveis/detalhes.html', {
        'imovel': imovel, 
        'is_favorito': is_favorito,
        'interesse': interesse_existente
    })

@login_required
def toggle_favorito(request, pk):
    if request.user.tipo_usuario != 'INQUILINO':
        return redirect('imoveis:detalhes', pk=pk)
        
    imovel = get_object_or_404(Imovel, pk=pk)
    
    favorito = Favorito.objects.filter(usuario=request.user, imovel=imovel).first()
    if favorito:
        favorito.delete()
    else:
        Favorito.objects.create(usuario=request.user, imovel=imovel)
    if request.POST.get('origem') == 'painel':
        return redirect('imoveis:meu_painel')
    return redirect('imoveis:detalhes', pk=pk)

@login_required
def demonstrar_interesse(request, pk):
    if request.user.tipo_usuario != 'INQUILINO':
        return redirect('imoveis:detalhes', pk=pk)

    imovel = get_object_or_404(Imovel, pk=pk)

    if Interesse.objects.filter(usuario=request.user, imovel=imovel).exists():
        return redirect('imoveis:detalhes', pk=pk)

    if request.method == 'POST':
        form = InteresseForm(request.POST)
        if form.is_valid():
            interesse = form.save(commit=False)
            interesse.usuario = request.user
            interesse.imovel = imovel
            interesse.status = 'PENDENTE'
            interesse.save()
            return redirect('imoveis:detalhes', pk=pk)
    else:
        form = InteresseForm()

    return render(request, 'imoveis/enviar_interesse.html', {'form': form, 'imovel': imovel})

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
    
    meus_favoritos = Favorito.objects.filter(usuario=request.user).select_related('imovel').order_by('-data_criacao')
    meus_interesses = Interesse.objects.filter(usuario=request.user).select_related('imovel').order_by('-data_criacao')
    
    return render(request, 'imoveis/painel_inquilino.html', {
        'favoritos': meus_favoritos,
        'interesses': meus_interesses
    })

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