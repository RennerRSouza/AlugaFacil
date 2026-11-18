from django import forms
from .models import Imovel, Interesse

class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = [
            'titulo', 'descricao', 'tipo', 'preco_aluguel', 'preco_condominio',
            'quartos', 'banheiros', 'vagas_garagem', 'area_m2',
            'cidade', 'bairro', 'rua', 'imagem_principal'
        ]

class InteresseForm(forms.ModelForm):
    class Meta:
        model = Interesse
        fields = ['mensagem']
        labels = {
            'mensagem': 'Mensagem para o Proprietário'
        }
        widgets = {
            'mensagem': forms.Textarea(attrs={'placeholder': 'Ex: Olá, tenho interesse neste imóvel. Podemos agendar uma visita?'})
        }