from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    class TipoUsuario(models.TextChoices):
        INQUILINO = 'INQUILINO', 'Inquilino'
        PROPRIETARIO = 'PROPRIETARIO', 'Proprietário'

    tipo_usuario = models.CharField(max_length=20,choices=TipoUsuario.choices,default=TipoUsuario.INQUILINO)
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"