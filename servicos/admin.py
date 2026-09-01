from django.contrib import admin
from servicos.models import Servico


class Servicos(admin.ModelAdmin):
    list_display = (
        'protocolo',
        'nome',
        'email',
        'telefone',
        'endereco',
        'problema',
        'status',
        'quantidade',
        'previsao_entrega',
        'criado_em',
        'notas',
    )

    list_display_links = (
        'protocolo',
        'nome',
    )

    list_per_page = 20

    search_fields = (
        'nome',
        'protocolo',
    )


admin.site.register(Servico, Servicos)
