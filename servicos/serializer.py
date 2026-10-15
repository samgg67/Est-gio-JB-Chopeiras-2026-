from rest_framework import serializers
from clientes.validadores import limpar_nome, limpar_problema, limpar_telefone, validar_previsao_entrega
from servicos.models import Servico

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = [
            'protocolo', 'nome', 'email', 'telefone', 'endereco', 'problema',
            'status', 'notas', 'quantidade', 'previsao_entrega', 'criado_em',
        ]
        read_only_fields = ['protocolo', 'criado_em']
        extra_kwargs = {'quantidade': {'min_value': 1}}

    def validate_nome(self, valor):
        return limpar_nome(valor)

    def validate_telefone(self, valor):
        return limpar_telefone(valor)

    def validate_problema(self, valor):
        return limpar_problema(valor)

    def validate_previsao_entrega(self, valor):
        if self.instance is None or valor != self.instance.previsao_entrega:
            validar_previsao_entrega(valor)
        return valor
