from django import forms
from .models import Imovel

class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = [
            'titulo', 'descricao', 'tipo', 'preco_aluguel', 'preco_condominio',
            'quartos', 'banheiros', 'vagas_garagem', 'area_m2',
            'cidade', 'bairro', 'rua', 'imagem_principal'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['style'] = 'width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px;'
            
        self.fields['descricao'].widget.attrs['rows'] = 4