from rest_framework import serializers
from clientes.models import Clientes

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
