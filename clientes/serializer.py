from rest_framework import serializers
from clientes.models import Clientes
from clientes.validadores import limpar_nome, limpar_telefone, validar_email_unico

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = [
            'id',
            'nome',
            'email',
            'telefone',
            'endereco',
            'tempo_de_fidelidade',
            'servicos_realizados',
        ]
        extra_kwargs = {
            'tempo_de_fidelidade': {'min_value': 0},
            'servicos_realizados': {'min_value': 0},
        }

    def validate_nome(self, valor):
        return limpar_nome(valor)

    def validate_email(self, valor):
        return validar_email_unico(valor, self.instance.pk if self.instance else None)

    def validate_telefone(self, valor):
        return limpar_telefone(valor)
