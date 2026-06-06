from django import forms
from .models import Servico

class ServicoFormulario(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'protocolo',
            'nome',
            'email',
            'telefone',
            'endereco',
            'problema',
            'status',
            'notas',
        ]