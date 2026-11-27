from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ImagemImovel, Imovel, Favorito, Interesse
from .forms import ImovelForm, InteresseForm
from usuarios.models import Usuario
from django.core.paginator import Paginator

def home(request):
    imoveis_queryset = Imovel.objects.filter(status='DISPONIVEL')

    busca = request.GET.get('busca', '').strip()
    tipo = request.GET.get('tipo', '')
    preco_min = request.GET.get('preco_min', '')
    preco_max = request.GET.get('preco_max', '')
    quartos = request.GET.get('quartos', '')
    banheiros = request.GET.get('banheiros', '')
    vagas = request.GET.get('vagas', '')
    area_min = request.GET.get('area_min', '')
    ordenar = request.GET.get('ordenar', 'recentes')

    if busca:
        imoveis_queryset = imoveis_queryset.filter(Q(cidade__icontains=busca) | Q(bairro__icontains=busca))
    if tipo:
        imoveis_queryset = imoveis_queryset.filter(tipo=tipo)
    if preco_min:
        imoveis_queryset = imoveis_queryset.filter(preco_aluguel__gte=preco_min)
    if preco_max:
        imoveis_queryset = imoveis_queryset.filter(preco_aluguel__lte=preco_max)
    if quartos:
        imoveis_queryset = imoveis_queryset.filter(quartos__gte=quartos)
    if banheiros:
        imoveis_queryset = imoveis_queryset.filter(banheiros__gte=banheiros)
    if vagas:
        imoveis_queryset = imoveis_queryset.filter(vagas_garagem__gte=vagas)
    if area_min:
        imoveis_queryset = imoveis_queryset.filter(area_m2__gte=area_min)

    opcoes_ordenacao = {
        'recentes': '-data_cadastro',
        'menor_preco': 'preco_aluguel',
        'maior_preco': '-preco_aluguel',
        'maior_area': '-area_m2',
    }
    imoveis_queryset = imoveis_queryset.order_by(opcoes_ordenacao.get(ordenar, '-data_cadastro'))

    paginator = Paginator(imoveis_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    tem_filtros_avancados = any([preco_min, quartos, banheiros, vagas, area_min, ordenar != 'recentes'])

    context = {
        'imoveis': page_obj,
        'page_obj': page_obj,
        'total_encontrados': paginator.count,
        'query_string': query_params.urlencode(),
        'tipos_imovel': Imovel.TipoImovel.choices,
        'tem_filtros_avancados': tem_filtros_avancados,
        'filtros': {
            'busca': busca,
            'tipo': tipo,
            'preco_min': preco_min,
            'preco_max': preco_max,
            'quartos': quartos,
            'banheiros': banheiros,
            'vagas': vagas,
            'area_min': area_min,
            'ordenar': ordenar,
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
        messages.success(request, 'Imóvel removido dos favoritos.')
    else:
        Favorito.objects.create(usuario=request.user, imovel=imovel)
        messages.success(request, 'Imóvel salvo nos favoritos!')
    if request.POST.get('origem') == 'painel':
        return redirect('imoveis:meu_painel')
    return redirect('imoveis:detalhes', pk=pk)

@login_required
def demonstrar_interesse(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)

    if imovel.proprietario == request.user:
        messages.error(request, 'Você não pode demonstrar interesse em seu próprio imóvel.')
        return redirect('imoveis:detalhes', pk=pk)

    if request.user.tipo_usuario != 'INQUILINO':
        messages.warning(request, 'Apenas contas de Inquilino podem enviar propostas.')
        return redirect('imoveis:detalhes', pk=pk)

    if imovel.status != 'DISPONIVEL':
        messages.warning(request, 'Este imóvel não está mais disponível para novas propostas.')
        return redirect('imoveis:detalhes', pk=pk)

    if Interesse.objects.filter(usuario=request.user, imovel=imovel).exists():
        messages.warning(request, 'Você já demonstrou interesse neste imóvel anteriormente.')
        return redirect('imoveis:detalhes', pk=pk)

    if request.method == 'POST':
        form = InteresseForm(request.POST)
        if form.is_valid():
            interesse = form.save(commit=False)
            interesse.usuario = request.user
            interesse.imovel = imovel
            interesse.status = 'PENDENTE'
            interesse.save()
            messages.success(request, 'Sua proposta foi enviada ao proprietário!')
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
            _salvar_imagens_extras(request, imovel)
            messages.success(request, 'Imóvel cadastrado com sucesso!')
            return redirect('imoveis:meu_painel')
    else:
        form = ImovelForm()
        
    return render(request, 'imoveis/novo_imovel.html', {'form': form})

@login_required
def meu_painel(request):
    # Painel Administrativo
    if request.user.is_staff:
        todos_usuarios = Usuario.objects.all().order_by('-date_joined')
        todos_imoveis = Imovel.objects.select_related('proprietario').all().order_by('-data_cadastro')
        todos_interesses = Interesse.objects.select_related('usuario', 'imovel').all().order_by('-data_criacao')
        
        return render(request, 'imoveis/painel_admin.html', {
            'usuarios': todos_usuarios,
            'imoveis': todos_imoveis,
            'interesses': todos_interesses,
            'status_choices': Imovel.StatusImovel.choices,
            'total_disponiveis': todos_imoveis.filter(status='DISPONIVEL').count(),
        })

    # Painel do Proprietário
    if request.user.tipo_usuario == 'PROPRIETARIO':
        meus_imoveis = Imovel.objects.filter(proprietario=request.user).order_by('-data_cadastro')
        interesses_recebidos = Interesse.objects.filter(imovel__proprietario=request.user).select_related('usuario', 'imovel').order_by('-data_criacao')
        
        return render(request, 'imoveis/painel_proprietario.html', {
            'imoveis': meus_imoveis,
            'interesses': interesses_recebidos,
            'status_choices': Imovel.StatusImovel.choices,
            'total_disponiveis': meus_imoveis.filter(status='DISPONIVEL').count(),
            'total_pendentes': interesses_recebidos.filter(status='PENDENTE').count(),
        })
    
    # Painel do Inquilino
    meus_favoritos = Favorito.objects.filter(usuario=request.user).select_related('imovel').order_by('-data_criacao')
    meus_interesses = Interesse.objects.filter(usuario=request.user).select_related('imovel').order_by('-data_criacao')
    
    return render(request, 'imoveis/painel_inquilino.html', {
        'favoritos': meus_favoritos,
        'interesses': meus_interesses
    })

@login_required
def responder_interesse(request, pk):
    if request.method == 'POST' and request.user.tipo_usuario == 'PROPRIETARIO':
        interesse = get_object_or_404(Interesse, pk=pk, imovel__proprietario=request.user)
        acao = request.POST.get('acao')
        
        if acao in ['ACEITO', 'RECUSADO']:
            interesse.status = acao
            interesse.save()
            messages.success(request, f'Proposta marcada como {interesse.get_status_display().lower()}.')
            
    return redirect('imoveis:meu_painel')

@login_required
def alterar_status_imovel(request, pk):
    if request.method == 'POST' and (request.user.tipo_usuario == 'PROPRIETARIO' or request.user.is_staff):
        if request.user.is_staff:
            imovel = get_object_or_404(Imovel, pk=pk)
        else:
            imovel = get_object_or_404(Imovel, pk=pk, proprietario=request.user)
            
        novo_status = request.POST.get('status')
        if novo_status in ['DISPONIVEL', 'RESERVADO', 'ALUGADO']:
            imovel.status = novo_status
            imovel.save()
            messages.success(request, f'Status alterado para {imovel.get_status_display()}.')
            
    return redirect('imoveis:meu_painel')

@login_required
def editar_imovel(request, pk):
    if request.user.is_staff:
        imovel = get_object_or_404(Imovel, pk=pk)
    else:
        imovel = get_object_or_404(Imovel, pk=pk, proprietario=request.user)
    
    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES, instance=imovel)
        if form.is_valid():
            form.save()
            _salvar_imagens_extras(request, imovel)
            messages.success(request, 'Alterações salvas com sucesso!')
            return redirect('imoveis:meu_painel')
    else:
        form = ImovelForm(instance=imovel)
        
    return render(request, 'imoveis/novo_imovel.html', {
        'form': form,
        'editando': True,
        'imovel': imovel
    })

@login_required
def excluir_imovel(request, pk):
    if request.user.is_staff:
        imovel = get_object_or_404(Imovel, pk=pk)
    else:
        imovel = get_object_or_404(Imovel, pk=pk, proprietario=request.user)
    
    if request.method == 'POST':
        imovel.delete()
        messages.success(request, 'Imóvel excluído com sucesso.')
        return redirect('imoveis:meu_painel')
        
    return render(request, 'imoveis/excluir_imovel.html', {'imovel': imovel})

@login_required
def cancelar_interesse(request, pk):
    if request.method == 'POST' and request.user.tipo_usuario == 'INQUILINO':
        interesse = get_object_or_404(
            Interesse,
            pk=pk,
            usuario=request.user,
            status='PENDENTE'
        )
        interesse.delete()
        messages.success(request, 'Proposta cancelada com sucesso.')
        
    return redirect('imoveis:meu_painel')

@login_required
def admin_excluir_usuario(request, pk):
    if not request.user.is_staff:
        return redirect('imoveis:home')

    usuario_alvo = get_object_or_404(Usuario, pk=pk)

    if usuario_alvo == request.user or usuario_alvo.is_superuser:
        messages.error(request, 'Não é permitido excluir sua própria conta de admin ou outro superusuário.')
        return redirect('imoveis:meu_painel')

    if request.method == 'POST':
        nome = usuario_alvo.username
        usuario_alvo.delete()
        messages.success(request, f'Usuário "{nome}" excluído com sucesso.')
        return redirect('imoveis:meu_painel')

    return render(request, 'usuarios/excluir_conta.html', {
        'usuario_alvo': usuario_alvo,
        'admin_excluindo': True
    })

@login_required
def excluir_foto_imovel(request, pk):
    if request.method == 'POST':
        foto = get_object_or_404(ImagemImovel, pk=pk)
        imovel = foto.imovel
        if imovel.proprietario == request.user or request.user.is_staff:
            foto.delete()
            messages.success(request, 'Foto removida da galeria.')
            return redirect('imoveis:editar_imovel', pk=imovel.id)
    return redirect('imoveis:meu_painel')

def _salvar_imagens_extras(request, imovel):
    limite_bytes = 5 * 1024 * 1024  # 5 MB
    for foto in request.FILES.getlist('imagens_extras'):
        if not foto.content_type.startswith('image/'):
            messages.warning(request, f'O arquivo "{foto.name}" foi ignorado por não ser uma imagem válida.')
            continue
        if foto.size > limite_bytes:
            messages.warning(request, f'A imagem "{foto.name}" ultrapassa o limite de 5 MB e foi ignorada.')
            continue
        ImagemImovel.objects.create(imovel=imovel, imagem=foto)