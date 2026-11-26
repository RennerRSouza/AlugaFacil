from django.contrib import admin
from .models import Imovel, ImagemImovel, Favorito, Interesse

class ImagemImovelInline(admin.TabularInline):
    model = ImagemImovel
    extra = 1

@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proprietario', 'tipo', 'cidade', 'preco_aluguel', 'status')
    list_filter = ('status', 'tipo', 'cidade')
    search_fields = ('titulo', 'cidade', 'bairro', 'proprietario__username')
    inlines = [ImagemImovelInline]

@admin.register(Interesse)
class InteresseAdmin(admin.ModelAdmin):
    list_display = ('imovel', 'usuario', 'status', 'data_criacao')
    list_filter = ('status',)

admin.site.register(Favorito)