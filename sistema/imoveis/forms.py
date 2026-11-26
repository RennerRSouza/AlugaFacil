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

    def clean_preco_aluguel(self):
        preco = self.cleaned_data.get('preco_aluguel')
        if preco is not None and preco <= 0:
            raise forms.ValidationError('O valor do aluguel deve ser maior que zero.')
        return preco

    def clean_preco_condominio(self):
        condominio = self.cleaned_data.get('preco_condominio')
        if condominio is not None and condominio < 0:
            raise forms.ValidationError('O valor do condomínio não pode ser negativo.')
        return condominio

    def clean_area_m2(self):
        area = self.cleaned_data.get('area_m2')
        if area is not None and area <= 0:
            raise forms.ValidationError('A área útil deve ser maior que zero.')
        return area

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