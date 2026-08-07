from django import forms
from .models import Servico


class ServicoFormulario(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'nome',
            'email',
            'telefone',
            'endereco',
            'problema',
            'status',
            'notas',
        ]

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()

        if not nome.replace(' ', '').isalpha():
            raise forms.ValidationError(
                'O nome deve conter apenas letras e espaços.'
            )

        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '').strip()

        if not telefone.isdigit():
            raise forms.ValidationError(
                'O telefone deve conter apenas números.'
            )

        return telefone