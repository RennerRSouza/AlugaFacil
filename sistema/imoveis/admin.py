from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Imovel, Favorito, Interesse

@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proprietario', 'tipo', 'preco_aluguel', 'status', 'cidade')
    list_filter = ('status', 'tipo', 'cidade')
    search_fields = ('titulo', 'descricao', 'cidade', 'bairro')

admin.site.register(Favorito)
admin.site.register(Interesse)