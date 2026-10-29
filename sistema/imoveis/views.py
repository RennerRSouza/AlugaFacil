from django.shortcuts import render,get_object_or_404
from .models import Imovel

def home(request):
    imoveis_lista = Imovel.objects.filter(status='DISPONIVEL').order_by('-data_cadastro')
    context = {
        'imoveis': imoveis_lista
    }  
    return render(request, 'imoveis/home.html', context)

def detalhes(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)   
    return render(request, 'imoveis/detalhes.html', {'imovel': imovel})