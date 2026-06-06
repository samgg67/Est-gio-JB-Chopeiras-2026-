from django import forms
from clientes.models import Clientes

class ClientesFormulario(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nome', 'email', 'telefone', 'endereco' , 'tempo_de_fidelidade', 'servicos_realizados']