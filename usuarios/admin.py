from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class CustomUsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'tipo_usuario', 'telefone', 'is_staff')
    list_filter = ('tipo_usuario', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações AlugaFácil', {'fields': ('tipo_usuario', 'telefone')}),
    )