from rest_framework import serializers
from clientes.models import Clientes

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = ['id', 'nome', 'email', 'telefone', 'endereco' , 'Tempo de fidelidade', 'servicos realizados']