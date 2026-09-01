from rest_framework import serializers
from servicos.models import Servico

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = [
            'protocolo', 'nome', 'email', 'telefone', 'endereco', 'problema',
            'status', 'notas', 'quantidade', 'previsao_entrega', 'criado_em',
        ]
        read_only_fields = ['protocolo', 'criado_em']
