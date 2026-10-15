from django.db import models
from django.conf import settings

class Imovel(models.Model):
    class TipoImovel(models.TextChoices):
        CASA = 'CASA', 'Casa'
        APARTAMENTO = 'APARTAMENTO', 'Apartamento'
        KITNET = 'KITNET', 'Kitnet'
        COMERCIAL = 'COMERCIAL', 'Sala Comercial'

    class StatusImovel(models.TextChoices):
        DISPONIVEL = 'DISPONIVEL', 'Disponível'
        RESERVADO = 'RESERVADO', 'Reservado'
        ALUGADO = 'ALUGADO', 'Alugado'

    proprietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='imoveis')
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(max_length=1000, blank=True)
    tipo = models.CharField(max_length=20, choices=TipoImovel.choices)
    preco_aluguel = models.DecimalField(max_digits=10, decimal_places=2)
    preco_condominio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quartos = models.PositiveIntegerField(default=1)
    banheiros = models.PositiveIntegerField(default=1)
    vagas_garagem = models.PositiveIntegerField(default=0)
    area_m2 = models.PositiveIntegerField(default=0)
    cidade = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    rua = models.CharField(max_length=150)
    imagem_principal = models.ImageField(upload_to='imoveis/', blank=True, null=True)
    status = models.CharField(max_length=20,choices=StatusImovel.choices,default=StatusImovel.DISPONIVEL)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.cidade}/{self.bairro}"

class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='favoritos')
    imovel = models.ForeignKey(Imovel,on_delete=models.CASCADE,related_name='favoritado_por')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'imovel')

    def __str__(self):
        return f"{self.usuario.username} -> {self.imovel.titulo}"


class Interesse(models.Model):
    class StatusInteresse(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        ACEITO = 'ACEITO', 'Aceito'
        RECUSADO = 'RECUSADO', 'Recusado'

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='interesses')
    imovel = models.ForeignKey(Imovel,on_delete=models.CASCADE,related_name='interessados')
    mensagem = models.TextField()
    status = models.CharField(max_length=20,choices=StatusInteresse.choices,default=StatusInteresse.PENDENTE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'imovel')

    def __str__(self):
        return f"Interesse de {self.usuario.username} no {self.imovel.titulo}"