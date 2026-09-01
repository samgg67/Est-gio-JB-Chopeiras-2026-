from django.contrib import admin

from .models import Clientes, LocalizacaoEmpresa, PerguntaFrequente


@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'usuario', 'ativo')
    search_fields = ('nome', 'email', 'telefone')


@admin.register(PerguntaFrequente)
class PerguntaFrequenteAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'ordem', 'ativa')
    list_editable = ('ordem', 'ativa')
    search_fields = ('pergunta', 'resposta')
    ordering = ('ordem', 'id')


@admin.register(LocalizacaoEmpresa)
class LocalizacaoEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'estado', 'telefone', 'ativa')
    list_filter = ('ativa', 'estado')
    search_fields = ('nome', 'endereco', 'cidade', 'telefone')
